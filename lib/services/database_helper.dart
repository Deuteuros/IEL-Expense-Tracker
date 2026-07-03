import 'dart:convert';
import 'dart:io';

import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';
import 'package:csv/csv.dart';
import '../models/transaction.dart';
import '../models/wallet.dart';

class DatabaseHelper {
  static final DatabaseHelper instance = DatabaseHelper._init();
  static Database? _database;

  DatabaseHelper._init();

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDB('cashew.db');
    return _database!;
  }

  Future<Database> _initDB(String filePath) async {
    final dbPath = await getDatabasesPath();
    final path = join(dbPath, filePath);

    return await openDatabase(
      path,
      version: 2,
      onCreate: _createDB,
      onUpgrade: _upgradeDB,
    );
  }

  Future _createDB(Database db, int version) async {
    // Table Wallets
    await db.execute('''
      CREATE TABLE wallets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        balance REAL DEFAULT 0
      )
    ''');

    // Default Wallet
    await db.insert('wallets', {'name': 'Caisse', 'balance': 0.0});

    // Table Transactions
    await db.execute('''
      CREATE TABLE transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        categorie_flux TEXT NOT NULL,
        item TEXT NOT NULL,
        quantite REAL,
        unite TEXT,
        prix_unitaire REAL,
        montant_total_mga REAL NOT NULL,
        fournisseur_client TEXT,
        portefeuille_id INTEGER,
        FOREIGN KEY (portefeuille_id) REFERENCES wallets(id)
      )
    ''');

    // Table Orders
    await db.execute('''
      CREATE TABLE orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_number TEXT NOT NULL,
        status TEXT NOT NULL,
        notes TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
      )
    ''');

    // Table Order Items
    await db.execute('''
      CREATE TABLE order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        quantity REAL NOT NULL,
        notes TEXT,
        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
      )
    ''');
  }

  Future _upgradeDB(Database db, int oldVersion, int newVersion) async {
    if (oldVersion < 2) {
      await db.execute('''
        CREATE TABLE orders (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          table_number TEXT NOT NULL,
          status TEXT NOT NULL,
          notes TEXT,
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL
        )
      ''');

      await db.execute('''
        CREATE TABLE order_items (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          order_id INTEGER NOT NULL,
          product_name TEXT NOT NULL,
          quantity REAL NOT NULL,
          notes TEXT,
          FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
        )
      ''');
    }
  }

  // --- Transactions CRUD ---

  Future<int> insertTransaction(TransactionModel transaction) async {
    final db = await instance.database;
    return await db.insert('transactions', transaction.toMap());
  }

  Future<int> deleteTransactions(List<int> ids) async {
    final db = await instance.database;
    return await db.delete(
      'transactions',
      where: 'id IN (${ids.join(',')})',
    );
  }

  Future<List<TransactionModel>> getAllTransactions() async {
    final db = await instance.database;
    final result = await db.query('transactions', orderBy: 'date DESC');
    return result.map((json) => TransactionModel.fromMap(json)).toList();
  }

  Future<List<TransactionModel>> getTransactionsByMonth(String monthStr) async {
    final db = await instance.database;
    final result = await db.query(
      'transactions',
      where: 'date LIKE ?',
      whereArgs: ['$monthStr%'],
      orderBy: 'date DESC',
    );
    return result.map((json) => TransactionModel.fromMap(json)).toList();
  }

  // --- Wallets CRUD ---

  Future<List<Wallet>> getAllWallets() async {
    final db = await instance.database;
    final result = await db.query('wallets');
    return result.map((json) => Wallet.fromMap(json)).toList();
  }

  // --- Stats / Summary ---

  Future<Map<String, double>> getSummary(int days) async {
    final db = await instance.database;
    final cutoffDate = DateTime.now().subtract(Duration(days: days)).toIso8601String().substring(0, 10);

    final incomeResult = await db.rawQuery(
      "SELECT SUM(montant_total_mga) as total FROM transactions WHERE date >= ? AND categorie_flux IN ('Miditra', 'Vente')",
      [cutoffDate],
    );
    final expenseResult = await db.rawQuery(
      "SELECT SUM(montant_total_mga) as total FROM transactions WHERE date >= ? AND categorie_flux IN ('Fandaniana', 'Achat')",
      [cutoffDate],
    );

    double income = incomeResult.first['total'] as double? ?? 0.0;
    double expense = expenseResult.first['total'] as double? ?? 0.0;

    return {
      'income': income,
      'expense': expense,
      'balance': income - expense,
    };
  }

  Future<List<String>> getMonthsWithData() async {
    final db = await instance.database;
    final result = await db.rawQuery(
      "SELECT DISTINCT strftime('%Y-%m', date) as month FROM transactions ORDER BY month DESC"
    );
    return result.map((row) => row['month'] as String).toList();
  }

  // --- CSV Import/Export ---

  Future<String> exportToCsv(String path) async {
    final db = await instance.database;
    final List<Map<String, dynamic>> querySnapshot = await db.query('transactions');
    
    List<List<dynamic>> rows = [];
    
    // Header
    if (querySnapshot.isNotEmpty) {
      rows.add(querySnapshot.first.keys.toList());
      
      for (var row in querySnapshot) {
        rows.add(row.values.toList());
      }
    }

    String csvData = ListToCsvConverter().convert(rows);
    final File file = File(path);
    await file.writeAsString(csvData);
    return path;
  }

  Future<int> importFromCsv(String path) async {
    final file = File(path);
    final bytes = await file.readAsBytes();
    String csvString = utf8.decode(bytes);
    
    // Remove BOM if present
    if (csvString.startsWith('\uFEFF')) {
      csvString = csvString.substring(1);
    }

    // Try to detect the separator (comma or semicolon)
    String separator = ',';
    final firstLine = csvString.split('\n').first;
    
    if (firstLine.contains(';') && !firstLine.contains(',')) {
      separator = ';';
    }

    // Normalize line endings to \n
    csvString = csvString.replaceAll('\r\n', '\n').replaceAll('\r', '\n');

    List<List<dynamic>> rowsAsListOfValues = CsvToListConverter(
      fieldDelimiter: separator,
      eol: '\n',
      shouldParseNumbers: true,
      allowInvalid: true,
    ).convert(csvString);

    if (rowsAsListOfValues.isEmpty) return 0;

    final db = await instance.database;
    
    // Process headers: trim them and convert to lowercase for comparison
    final rawHeader = rowsAsListOfValues.first;
    final List<String> header = rawHeader.map((h) => h.toString().trim().toLowerCase()).toList();
    
    int importedCount = 0;

    // Get wallets to map names to IDs
    final List<Map<String, dynamic>> wallets = await db.query('wallets');
    final Map<String, int> walletMap = {
      for (var w in wallets) w['name'].toString().toLowerCase(): w['id'] as int
    };

    await db.transaction((txn) async {
      for (int i = 1; i < rowsAsListOfValues.length; i++) {
        final row = rowsAsListOfValues[i];
        if (row.length < header.length) continue; // Skip incomplete rows

        Map<String, dynamic> data = {};
        for (int j = 0; j < header.length; j++) {
          String key = header[j];
          var value = row[j];
          
          if (key == 'id') continue;
          
          // Mapping from CSV names to SQLite column names
          if (key == 'portefeuille') {
            final walletName = value.toString().trim().toLowerCase();
            key = 'portefeuille_id';
            value = walletMap[walletName] ?? (walletMap.isNotEmpty ? walletMap.values.first : 1);
          }
          
          // Handle specific column names if they differ
          if (key == 'category_flux') key = 'categorie_flux';
          if (key == 'quantity') key = 'quantite';
          if (key == 'unit') key = 'unite';
          if (key == 'unit_price') key = 'prix_unitaire';
          if (key == 'total_amount_mga') key = 'montant_total_mga';
          if (key == 'provider_client') key = 'fournisseur_client';

          // Clean up values
          if (value is String) {
            value = value.trim();
            if (value.isEmpty) value = null;
          }
          
          // Ensure numeric values are actually numbers
          if (['quantite', 'prix_unitaire', 'montant_total_mga'].contains(key)) {
            if (value is String) {
              value = double.tryParse(value.replaceAll(',', '.'));
            }
          }
          
          data[key] = value;
        }
        
        // Final sanity check: ensure montant_total_mga is present and valid
        if (data['montant_total_mga'] != null && data['date'] != null) {
          try {
            await txn.insert('transactions', data);
            importedCount++;
          } catch (_) {
            // Silently skip duplicates or errors in final version
          }
        }
      }
    });

    return importedCount;
  }

  // --- Statistics for Charts ---

  Future<List<Map<String, dynamic>>> getEvolutionData(int days) async {
    final db = await instance.database;
    final cutoffDate = DateTime.now().subtract(Duration(days: days)).toIso8601String().substring(0, 10);

    final query = """
        SELECT date, 
               SUM(CASE WHEN categorie_flux IN ('Miditra', 'Vente') THEN montant_total_mga ELSE -montant_total_mga END) as daily_net 
        FROM transactions 
        WHERE date >= ? 
        GROUP BY date 
        ORDER BY date ASC
    """;
    
    final List<Map<String, dynamic>> result = await db.rawQuery(query, [cutoffDate]);
    
    double cumulativeBalance = 0;
    List<Map<String, dynamic>> evolution = [];
    
    for (var row in result) {
      cumulativeBalance += (row['daily_net'] as num).toDouble();
      evolution.add({
        'date': row['date'],
        'balance': cumulativeBalance,
      });
    }
    
    return evolution;
  }

  Future<List<Map<String, dynamic>>> getDistributionData(int days) async {
    final db = await instance.database;
    final cutoffDate = DateTime.now().subtract(Duration(days: days)).toIso8601String().substring(0, 10);

    final query = """
        SELECT item, SUM(montant_total_mga) as total 
        FROM transactions 
        WHERE date >= ? AND categorie_flux IN ('Fandaniana', 'Achat') 
        GROUP BY item 
        ORDER BY total DESC 
        LIMIT 5
    """;
    
    final List<Map<String, dynamic>> result = await db.rawQuery(query, [cutoffDate]);
    return result;
  }

  // --- Suggestions for Smart Entry ---

  Future<List<String>> getDistinctItems() async {
    final db = await instance.database;
    final result = await db.rawQuery(
      "SELECT DISTINCT item FROM transactions WHERE item IS NOT NULL AND item != '' ORDER BY item ASC"
    );
    return result.map((row) => row['item'] as String).toList();
  }

  Future<List<String>> getDistinctClients() async {
    final db = await instance.database;
    final result = await db.rawQuery(
      "SELECT DISTINCT fournisseur_client FROM transactions WHERE fournisseur_client IS NOT NULL AND fournisseur_client != '' ORDER BY fournisseur_client ASC"
    );
    return result.map((row) => row['fournisseur_client'] as String).toList();
  }

  Future<String?> getRecentUnitForItem(String item) async {
    final db = await instance.database;
    final result = await db.rawQuery(
      "SELECT unite FROM transactions WHERE item = ? AND unite IS NOT NULL AND unite != '' ORDER BY date DESC, id DESC LIMIT 1",
      [item]
    );
    if (result.isNotEmpty) {
      return result.first['unite'] as String?;
    }
    return null;
  }

  // --- Orders CRUD ---

  Future<int> insertOrder(Map<String, dynamic> orderData, List<Map<String, dynamic>> itemsData) async {
    final db = await instance.database;
    return await db.transaction((txn) async {
      final orderId = await txn.insert('orders', orderData);
      for (var item in itemsData) {
        await txn.insert('order_items', {
          ...item,
          'order_id': orderId,
        });
      }
      return orderId;
    });
  }

  Future<int> updateOrderStatus(int orderId, String status) async {
    final db = await instance.database;
    return await db.update(
      'orders',
      {
        'status': status,
        'updated_at': DateTime.now().toIso8601String(),
      },
      where: 'id = ?',
      whereArgs: [orderId],
    );
  }

  Future<List<Map<String, dynamic>>> getOrders() async {
    final db = await instance.database;
    final List<Map<String, dynamic>> ordersResult = await db.query('orders', orderBy: 'created_at DESC');
    List<Map<String, dynamic>> detailedOrders = [];
    for (var order in ordersResult) {
      final List<Map<String, dynamic>> itemsResult = await db.query(
        'order_items',
        where: 'order_id = ?',
        whereArgs: [order['id']],
      );
      detailedOrders.add({
        ...order,
        'items': itemsResult,
      });
    }
    return detailedOrders;
  }

  Future close() async {
    final db = await instance.database;
    db.close();
  }
}
