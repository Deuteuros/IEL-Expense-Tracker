class OrderServerItem {
  final int? id;
  final int? orderId;
  final String productName;
  final double quantity;
  final String? notes;

  OrderServerItem({
    this.id,
    this.orderId,
    required this.productName,
    required this.quantity,
    this.notes,
  });

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'order_id': orderId,
      'product_name': productName,
      'quantity': quantity,
      'notes': notes,
    };
  }

  factory OrderServerItem.fromMap(Map<String, dynamic> map) {
    return OrderServerItem(
      id: map['id'],
      orderId: map['order_id'],
      productName: map['product_name'] ?? '',
      quantity: (map['quantity'] as num?)?.toDouble() ?? 0.0,
      notes: map['notes'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'item_id': id,
      'product_name': productName,
      'quantity': quantity,
      'notes': notes ?? '',
    };
  }
}

class OrderServerModel {
  final int? id;
  final String tableNumber;
  final String status;
  final String? notes;
  final String createdAt;
  final String updatedAt;
  final List<OrderServerItem> items;

  OrderServerModel({
    this.id,
    required this.tableNumber,
    required this.status,
    this.notes,
    required this.createdAt,
    required this.updatedAt,
    required this.items,
  });

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'table_number': tableNumber,
      'status': status,
      'notes': notes,
      'created_at': createdAt,
      'updated_at': updatedAt,
    };
  }

  factory OrderServerModel.fromMap(Map<String, dynamic> map) {
    var itemsList = (map['items'] as List?) ?? [];
    return OrderServerModel(
      id: map['id'],
      tableNumber: map['table_number'] ?? '',
      status: map['status'] ?? 'A_FAIRE',
      notes: map['notes'],
      createdAt: map['created_at'] ?? '',
      updatedAt: map['updated_at'] ?? '',
      items: itemsList.map((item) => OrderServerItem.fromMap(item)).toList(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'order_id': id,
      'table_number': tableNumber,
      'status': status,
      'notes': notes ?? '',
      'created_at': createdAt,
      'items': items.map((item) => item.toJson()).toList(),
    };
  }
}
