import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../providers/transaction_provider.dart';
import '../models/transaction.dart';
import '../services/database_helper.dart';

final selectedMonthProvider = StateProvider<String?>((ref) => null);
final selectedIdsProvider = StateProvider<Set<int>>((ref) => {});

class HistoryView extends ConsumerWidget {
  const HistoryView({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final transactionsAsync = ref.watch(transactionsProvider);
    final selectedMonth = ref.watch(selectedMonthProvider);
    final selectedIds = ref.watch(selectedIdsProvider);
    final isSelectionMode = selectedIds.isNotEmpty;
    final numberFormat = NumberFormat("#,##0", "fr_FR");

    return Scaffold(
      appBar: AppBar(
        leading: isSelectionMode 
          ? IconButton(
              icon: const Icon(Icons.close),
              onPressed: () => ref.read(selectedIdsProvider.notifier).state = {},
            )
          : null,
        title: isSelectionMode 
          ? Text('${selectedIds.length} voafidy')
          : Text(selectedMonth == null ? 'Tantara' : 'Tantara ($selectedMonth)'),
        centerTitle: true,
        actions: [
          if (isSelectionMode)
            IconButton(
              icon: const Icon(Icons.delete, color: Colors.red),
              onPressed: () => _confirmDeletion(context, ref, selectedIds),
            )
          else
            IconButton(
              icon: Icon(selectedMonth == null ? Icons.filter_list : Icons.filter_list_off),
              onPressed: () {
                if (selectedMonth != null) {
                  ref.read(selectedMonthProvider.notifier).state = null;
                } else {
                  _showMonthPicker(context, ref);
                }
              },
            ),
        ],
      ),
      body: transactionsAsync.when(
        data: (transactions) {
          final filtered = selectedMonth == null 
            ? transactions 
            : transactions.where((t) => t.date.startsWith(selectedMonth)).toList();

          if (filtered.isEmpty) {
            return const Center(child: Text('Tsy misy hara-mira (Aucune transaction)'));
          }

          return ListView.separated(
            padding: const EdgeInsets.all(8),
            itemCount: filtered.length,
            separatorBuilder: (context, index) => const Divider(height: 1),
            itemBuilder: (context, index) {
              final t = filtered[index];
              final isSelected = selectedIds.contains(t.id);
              
              return InkWell(
                onLongPress: () {
                  if (t.id != null) {
                    ref.read(selectedIdsProvider.notifier).update((state) => {...state, t.id!});
                  }
                },
                onTap: () {
                  if (isSelectionMode && t.id != null) {
                    ref.read(selectedIdsProvider.notifier).update((state) {
                      if (state.contains(t.id)) {
                        return state.where((id) => id != t.id).toSet();
                      } else {
                        return {...state, t.id!};
                      }
                    });
                  }
                },
                child: _buildTransactionTile(t, numberFormat, isSelected, isSelectionMode),
              );
            },
          );
        },
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, stack) => Center(child: Text('Erreur: $err')),
      ),
    );
  }

  Future<void> _confirmDeletion(BuildContext context, WidgetRef ref, Set<int> ids) async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Hamafa hara-mira'),
        content: Text('Tena hamafa ireo hara-mira ${ids.length} ireo ve ianao ?'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context, false), child: const Text('Hanafoana')),
          FilledButton(
            onPressed: () => Navigator.pop(context, true), 
            style: FilledButton.styleFrom(backgroundColor: Colors.red),
            child: const Text('Eny, fafao'),
          ),
        ],
      ),
    );

    if (confirmed == true) {
      await DatabaseHelper.instance.deleteTransactions(ids.toList());
      ref.read(selectedIdsProvider.notifier).state = {};
      ref.invalidate(transactionsProvider);
      ref.invalidate(summaryProvider);
      ref.invalidate(evolutionProvider);
      ref.invalidate(distributionProvider);
      ref.invalidate(monthsProvider);
    }
  }

  void _showMonthPicker(BuildContext context, WidgetRef ref) {
    final monthsAsync = ref.watch(monthsProvider);

    showModalBottomSheet(
      context: context,
      builder: (context) {
        return monthsAsync.when(
          data: (months) => Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Padding(
                padding: EdgeInsets.all(16.0),
                child: Text('Safidio ny volana', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
              ),
              Expanded(
                child: ListView.builder(
                  itemCount: months.length,
                  itemBuilder: (context, index) {
                    final m = months[index];
                    return ListTile(
                      title: Text(m),
                      onTap: () {
                        ref.read(selectedMonthProvider.notifier).state = m;
                        Navigator.pop(context);
                      },
                    );
                  },
                ),
              ),
            ],
          ),
          loading: () => const Center(child: CircularProgressIndicator()),
          error: (e, s) => Center(child: Text('Error: $e')),
        );
      },
    );
  }

  Widget _buildTransactionTile(TransactionModel t, NumberFormat fmt, bool isSelected, bool isSelectionMode) {
    final isExpense = t.categoryFlux == 'Fandaniana' || t.categoryFlux == 'Achat';
    final color = isExpense ? Colors.red : Colors.green;
    final icon = isExpense ? Icons.remove_circle_outline : Icons.add_circle_outline;

    return Container(
      color: isSelected ? color.withOpacity(0.1) : null,
      child: ListTile(
        leading: isSelectionMode 
          ? Checkbox(value: isSelected, onChanged: (val) {})
          : CircleAvatar(
              backgroundColor: color.withOpacity(0.1),
              child: Icon(icon, color: color),
            ),
        title: Text(t.item, style: const TextStyle(fontWeight: FontWeight.bold)),
        subtitle: Text('${t.date} • ${t.providerClient ?? "Divers"}'),
        trailing: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.end,
          children: [
            Text(
              '${isExpense ? "-" : "+"}${fmt.format(t.totalAmountMga).replaceAll(',', ' ')} Ar',
              style: TextStyle(
                fontWeight: FontWeight.bold,
                color: color,
                fontSize: 14,
              ),
            ),
            if (t.quantity != null && t.quantity! > 0)
              Text(
                '${t.quantity} ${t.unit ?? ""}',
                style: const TextStyle(fontSize: 10, color: Colors.grey),
              ),
          ],
        ),
      ),
    );
  }
}
