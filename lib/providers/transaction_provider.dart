import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/transaction.dart';
import '../services/database_helper.dart';

final transactionsProvider = FutureProvider<List<TransactionModel>>((ref) async {
  return await DatabaseHelper.instance.getAllTransactions();
});

final summaryProvider = FutureProvider<Map<String, double>>((ref) async {
  return await DatabaseHelper.instance.getSummary(30); // 30 days
});

final monthsProvider = FutureProvider<List<String>>((ref) async {
  return await DatabaseHelper.instance.getMonthsWithData();
});

final evolutionProvider = FutureProvider<List<Map<String, dynamic>>>((ref) async {
  return await DatabaseHelper.instance.getEvolutionData(30);
});

final distributionProvider = FutureProvider<List<Map<String, dynamic>>>((ref) async {
  return await DatabaseHelper.instance.getDistributionData(30);
});
