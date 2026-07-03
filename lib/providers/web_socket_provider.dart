import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../services/network/web_socket_server_manager.dart';

final webSocketServerProvider = ChangeNotifierProvider<WebSocketServerManager>((ref) {
  final manager = WebSocketServerManager();
  
  // Start server on initialization
  manager.start().catchError((e) {
    print('Failed to auto-start WebSocket server: $e');
  });

  ref.onDispose(() {
    manager.stop();
  });
  
  return manager;
});
