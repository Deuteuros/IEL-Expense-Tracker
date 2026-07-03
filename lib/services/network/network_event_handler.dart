import 'dart:convert';
import '../../models/order.dart';
import '../database_helper.dart';

final List<Map<String, dynamic>> menuProducts = [
  {"id": "m1", "name": "Ravitoto sy Hena-kisoa", "price": 20000.0, "category": "Sakafo Malagasy", "unit": "Portion"},
  {"id": "m2", "name": "Henan'omby sy Tsaramaso", "price": 18000.0, "category": "Sakafo Malagasy", "unit": "Portion"},
  {"id": "m3", "name": "Hena kisoa sy Sakamalaho", "price": 22000.0, "category": "Sakafo Malagasy", "unit": "Portion"},
  {"id": "m4", "name": "Romazava Hena sy Anana", "price": 16000.0, "category": "Sakafo Malagasy", "unit": "Portion"},
  {"id": "e1", "name": "Steak Frites", "price": 25000.0, "category": "Sakafo Eoropeana", "unit": "Assiette"},
  {"id": "e2", "name": "Poulet Rôti salade", "price": 24000.0, "category": "Sakafo Eoropeana", "unit": "Portion"},
  {"id": "e3", "name": "Pâtes Carbonara", "price": 22000.0, "category": "Sakafo Eoropeana", "unit": "Assiette"},
  {"id": "e4", "name": "Poisson Meunière", "price": 28000.0, "category": "Sakafo Eoropeana", "unit": "Assiette"},
  {"id": "p1", "name": "Pizza Margherita", "price": 18000.0, "category": "Piza", "unit": "Pièce"},
  {"id": "p2", "name": "Pizza Reine", "price": 22000.0, "category": "Piza", "unit": "Pièce"},
  {"id": "p3", "name": "Pizza Quatre Saisons", "price": 24000.0, "category": "Piza", "unit": "Pièce"},
  {"id": "p4", "name": "Pizza Spéciale Maison", "price": 26000.0, "category": "Piza", "unit": "Pièce"},
  {"id": "d1", "name": "Ranovola (Ampango)", "price": 2000.0, "category": "Zava-pisotro", "unit": "Verre"},
  {"id": "d2", "name": "Jus de fruits frais", "price": 6000.0, "category": "Zava-pisotro", "unit": "Verre"},
  {"id": "d3", "name": "Coca-Cola / Fanta", "price": 4500.0, "category": "Zava-pisotro", "unit": "Bouteille"},
  {"id": "d4", "name": "Bière THB local", "price": 7000.0, "category": "Zava-pisotro", "unit": "Bouteille"},
  {"id": "t1", "name": "Sambosa Hena (Sambos)", "price": 4000.0, "category": "Tsakitsaky", "unit": "Portion"},
  {"id": "t2", "name": "Nems Légumes", "price": 5000.0, "category": "Tsakitsaky", "unit": "Portion"},
  {"id": "t3", "name": "Mofo baolina mafana", "price": 3000.0, "category": "Tsakitsaky", "unit": "Portion"},
];

String getProductName(String productId) {
  final product = menuProducts.firstWhere(
    (p) => p['id'].toString() == productId,
    orElse: () => {"name": "Produit Inconnu ($productId)"},
  );
  return product['name'] as String;
}

class NetworkEventHandler {
  final void Function(String message) broadcastMessage;

  NetworkEventHandler({required this.broadcastMessage});

  Future<void> handleMessage(String rawMessage) async {
    try {
      final Map<String, dynamic> message = jsonDecode(rawMessage);
      final String? type = message['type'];
      final Map<String, dynamic>? payload = message['payload'];

      if (type == null || payload == null) return;

      switch (type) {
        case 'PLACE_ORDER':
          await _handlePlaceOrder(payload);
          break;
        case 'UPDATE_STATUS':
          await _handleUpdateStatus(payload);
          break;
        default:
          print('Unsupported message type: $type');
      }
    } catch (e) {
      print('Error parsing message: $e');
    }
  }

  Future<void> _handlePlaceOrder(Map<String, dynamic> payload) async {
    final String tableNumber = payload['table_number'] ?? '';
    final String notes = payload['notes'] ?? '';
    final List<dynamic> itemsData = payload['items'] ?? [];

    final String nowStr = DateTime.now().toIso8601String();

    final orderData = {
      'table_number': tableNumber,
      'status': 'A_FAIRE',
      'notes': notes,
      'created_at': nowStr,
      'updated_at': nowStr,
    };

    final List<Map<String, dynamic>> itemsList = [];
    for (var item in itemsData) {
      final String productId = item['product_id']?.toString() ?? '';
      final double quantity = (item['quantity'] as num?)?.toDouble() ?? 0.0;
      final String itemNotes = item['notes'] ?? '';

      itemsList.add({
        'product_name': getProductName(productId),
        'quantity': quantity,
        'notes': itemNotes,
      });
    }

    // Insert into DB
    final int orderId = await DatabaseHelper.instance.insertOrder(orderData, itemsList);

    // Broadcast ORDER_CREATED to all clients
    final response = {
      "type": "ORDER_CREATED",
      "sender": "CASH",
      "timestamp": nowStr,
      "payload": {
        "order_id": orderId,
        "table_number": tableNumber,
        "status": "A_FAIRE",
        "notes": notes,
        "created_at": nowStr,
        "items": itemsList.asMap().entries.map((entry) {
          int idx = entry.key;
          var item = entry.value;
          return {
            "item_id": idx + 1,
            "product_name": item['product_name'],
            "quantity": item['quantity'],
            "notes": item['notes']
          };
        }).toList()
      }
    };

    broadcastMessage(jsonEncode(response));
  }

  Future<void> _handleUpdateStatus(Map<String, dynamic> payload) async {
    final int orderId = int.tryParse(payload['order_id'].toString()) ?? 0;
    final String status = payload['status'] ?? 'A_FAIRE';

    if (orderId == 0) return;

    // Update in DB
    await DatabaseHelper.instance.updateOrderStatus(orderId, status);

    final String nowStr = DateTime.now().toIso8601String();

    // Broadcast STATUS_UPDATED
    final response = {
      "type": "STATUS_UPDATED",
      "sender": "CASH",
      "timestamp": nowStr,
      "payload": {
        "order_id": orderId,
        "status": status,
        "updated_at": nowStr
      }
    };

    broadcastMessage(jsonEncode(response));
  }
}
