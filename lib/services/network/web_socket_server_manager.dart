import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:shelf/shelf.dart' as shelf;
import 'package:shelf/shelf_io.dart' as shelf_io;
import 'package:shelf_router/shelf_router.dart';
import 'package:shelf_web_socket/shelf_web_socket.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import '../database_helper.dart';
import 'network_event_handler.dart';

class WebSocketServerManager extends ChangeNotifier {
  HttpServer? _server;
  final Set<WebSocketChannel> _clients = {};
  late final NetworkEventHandler _eventHandler;
  
  bool _isRunning = false;
  String? _ipAddress;
  final int _port = 8080;

  WebSocketServerManager() {
    _eventHandler = NetworkEventHandler(broadcastMessage: broadcast);
  }

  bool get isRunning => _isRunning;
  String? get ipAddress => _ipAddress;
  int get port => _port;
  int get connectedClientsCount => _clients.length;

  Future<void> start() async {
    if (_isRunning) return;

    try {
      _ipAddress = await _getLocalIpAddress();
      
      final router = Router();
      
      router.get('/ws', webSocketHandler((WebSocketChannel webSocket) {
        _clients.add(webSocket);
        notifyListeners();

        // 1. Send SYNC_MENU upon connection
        final syncMenuMsg = {
          "type": "SYNC_MENU",
          "sender": "CASH",
          "timestamp": DateTime.now().toIso8601String(),
          "payload": {
            "products": menuProducts
          }
        };
        webSocket.sink.add(jsonEncode(syncMenuMsg));

        // 2. Fetch and send all active orders (status != 'PAYE')
        _syncActiveOrdersToClient(webSocket);

        webSocket.stream.listen(
          (message) {
            _eventHandler.handleMessage(message.toString());
          },
          onDone: () {
            _clients.remove(webSocket);
            notifyListeners();
          },
          onError: (error) {
            _clients.remove(webSocket);
            notifyListeners();
          },
        );
      }));

      _server = await shelf_io.serve(router, InternetAddress.anyIPv4, _port);
      _isRunning = true;
      notifyListeners();
      print('WebSocket Server started on ws://$_ipAddress:$_port/ws');
    } catch (e) {
      print('Error starting WebSocket Server: $e');
      _isRunning = false;
      _ipAddress = null;
      notifyListeners();
      rethrow;
    }
  }

  Future<void> stop() async {
    if (!_isRunning) return;

    for (var client in _clients) {
      try {
        await client.sink.close();
      } catch (_) {}
    }
    _clients.clear();

    await _server?.close(force: true);
    _server = null;
    _isRunning = false;
    _ipAddress = null;
    notifyListeners();
    print('WebSocket Server stopped.');
  }

  void broadcast(String message) {
    for (var client in _clients) {
      try {
        client.sink.add(message);
      } catch (e) {
        print('Error broadcasting to client: $e');
      }
    }
  }

  Future<void> _syncActiveOrdersToClient(WebSocketChannel client) async {
    try {
      final List<Map<String, dynamic>> rawOrders = await DatabaseHelper.instance.getOrders();
      for (var order in rawOrders) {
        if (order['status'] == 'PAYE') continue;

        final response = {
          "type": "ORDER_CREATED",
          "sender": "CASH",
          "timestamp": order['created_at'],
          "payload": {
            "order_id": order['id'],
            "table_number": order['table_number'],
            "status": order['status'],
            "notes": order['notes'] ?? '',
            "created_at": order['created_at'],
            "items": (order['items'] as List<dynamic>? ?? []).asMap().entries.map((entry) {
              int idx = entry.key;
              var item = entry.value;
              return {
                "item_id": item['id'] ?? (idx + 1),
                "product_name": item['product_name'],
                "quantity": (item['quantity'] as num?)?.toDouble() ?? 0.0,
                "notes": item['notes'] ?? ''
              };
            }).toList()
          }
        };
        client.sink.add(jsonEncode(response));
      }
    } catch (e) {
      print('Error syncing active orders: $e');
    }
  }

  void notifyPayment(int orderId, double amountMga) {
    final nowStr = DateTime.now().toIso8601String();
    final paymentMsg = {
      "type": "ORDER_PAID",
      "sender": "CASH",
      "timestamp": nowStr,
      "payload": {
        "order_id": orderId,
        "status": "PAYE",
        "amount_mga": amountMga
      }
    };
    broadcast(jsonEncode(paymentMsg));
  }

  Future<String> _getLocalIpAddress() async {
    try {
      final interfaces = await NetworkInterface.list(
        includeLoopback: false,
        type: InternetAddressType.IPv4,
      );
      
      for (var interface in interfaces) {
        for (var addr in interface.addresses) {
          if (!addr.isLoopback && (addr.address.startsWith('192.168.') || addr.address.startsWith('10.') || addr.address.startsWith('172.'))) {
            return addr.address;
          }
        }
      }
      
      for (var interface in interfaces) {
        for (var addr in interface.addresses) {
          if (!addr.isLoopback) {
            return addr.address;
          }
        }
      }
    } catch (e) {
      print('Error getting local IP: $e');
    }
    return '127.0.0.1';
  }
}
