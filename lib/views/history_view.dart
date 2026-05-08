import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../providers/transaction_provider.dart';
import '../models/transaction.dart';
import '../services/database_helper.dart';

final selectedMonthProvider = StateProvider<String?>((ref) => null);
final selectedIdsProvider = StateProvider<Set<int>>((ref) => {});
final searchQueryProvider = StateProvider<String>((ref) => "");
final isSearchingProvider = StateProvider<bool>((ref) => false);

class HistoryView extends ConsumerWidget {
  const HistoryView({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final transactionsAsync = ref.watch(transactionsProvider);
    final selectedMonth = ref.watch(selectedMonthProvider);
    final selectedIds = ref.watch(selectedIdsProvider);
    final monthsAsync = ref.watch(monthsProvider);
    final isSearching = ref.watch(isSearchingProvider);
    final searchQuery = ref.watch(searchQueryProvider).toLowerCase();

    // Auto-select latest month if none selected
    ref.listen(monthsProvider, (previous, next) {
      if (next is AsyncData && selectedMonth == null && !isSearching) {
        final months = next.value;
        if (months != null && months.isNotEmpty) {
          ref.read(selectedMonthProvider.notifier).state = months.first;
        }
      }
    });

    final isSelectionMode = selectedIds.isNotEmpty;
    final numberFormat = NumberFormat("#,##0", "fr_FR");

    return Scaffold(
      appBar: AppBar(
        leading: isSelectionMode 
          ? IconButton(
              icon: const Icon(Icons.close),
              onPressed: () => ref.read(selectedIdsProvider.notifier).state = {},
            )
          : (isSearching ? IconButton(
              icon: const Icon(Icons.arrow_back),
              onPressed: () {
                ref.read(isSearchingProvider.notifier).state = false;
                ref.read(searchQueryProvider.notifier).state = "";
              },
            ) : null),
        title: isSelectionMode 
          ? Text('${selectedIds.length} voafidy')
          : (isSearching 
              ? TextField(
                  autofocus: true,
                  decoration: const InputDecoration(
                    hintText: 'Hikaroka (nom, date YYYY-MM-DD)...',
                    border: InputBorder.none,
                  ),
                  onChanged: (val) => ref.read(searchQueryProvider.notifier).state = val,
                )
              : const Text('Tantara')),
        centerTitle: !isSearching,
        actions: [
          if (isSelectionMode)
            IconButton(
              icon: const Icon(Icons.delete, color: Colors.red),
              onPressed: () => _confirmDeletion(context, ref, selectedIds),
            )
          else
            IconButton(
              icon: Icon(isSearching ? Icons.close : Icons.search),
              onPressed: () {
                if (isSearching) {
                  ref.read(isSearchingProvider.notifier).state = false;
                  ref.read(searchQueryProvider.notifier).state = "";
                } else {
                  ref.read(isSearchingProvider.notifier).state = true;
                }
              },
            ),
        ],
      ),
      body: Column(
        children: [
          if (!isSearching) _buildMonthSelector(ref, monthsAsync, selectedMonth),
          transactionsAsync.when(
            data: (transactions) {
              final filtered = transactions.where((t) {
                // Apply search filter if active
                if (isSearching && searchQuery.isNotEmpty) {
                  final matchesName = t.item.toLowerCase().contains(searchQuery);
                  final matchesDate = t.date.contains(searchQuery);
                  return matchesName || matchesDate;
                }
                // Otherwise apply month filter
                if (selectedMonth != null) {
                  return t.date.startsWith(selectedMonth);
                }
                return true;
              }).toList();

              return Expanded(
                child: Column(
                  children: [
                    if (selectedMonth != null) _buildSummaryBar(filtered, numberFormat),
                    if (filtered.isEmpty)
                      const Expanded(child: Center(child: Text('Tsy misy hara-mira (Aucune transaction)')))
                    else
                      Expanded(
                        child: _buildGroupedTransactionList(filtered, numberFormat, selectedIds, isSelectionMode, ref),
                      ),
                  ],
                ),
              );
            },
            loading: () => const Expanded(child: Center(child: CircularProgressIndicator())),
            error: (err, stack) => Expanded(child: Center(child: Text('Erreur: $err'))),
          ),
        ],
      ),
    );
  }

  static const _monthsMg = {
    1: "Janoary", 2: "Febroary", 3: "Martsa", 4: "Aprily",
    5: "Mey", 6: "Jona", 7: "Jolay", 8: "Aogositra",
    9: "Septambra", 10: "Oktobra", 11: "Novambra", 12: "Desambra"
  };

  String _formatMonthLabel(String monthStr) {
    try {
      final parts = monthStr.split('-');
      final year = parts[0];
      final month = int.parse(parts[1]);
      return '${_monthsMg[month]} $year'.toLowerCase();
    } catch (e) {
      return monthStr;
    }
  }

  Widget _buildMonthSelector(WidgetRef ref, AsyncValue<List<String>> monthsAsync, String? selectedMonth) {
    return monthsAsync.when(
      data: (months) => Container(
        height: 50,
        padding: const EdgeInsets.symmetric(vertical: 8),
        child: ListView.builder(
          scrollDirection: Axis.horizontal,
          itemCount: months.length,
          itemBuilder: (context, index) {
            final m = months[index];
            final isSelected = m == selectedMonth;
            return InkWell(
              onTap: () => ref.read(selectedMonthProvider.notifier).state = m,
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16),
                child: Column(
                  children: [
                    Text(
                      _formatMonthLabel(m),
                      style: TextStyle(
                        fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                        color: isSelected ? Colors.black : Colors.grey,
                        fontSize: 16,
                      ),
                    ),
                    if (isSelected)
                      Container(
                        height: 3,
                        width: 40,
                        margin: const EdgeInsets.only(top: 4),
                        decoration: BoxDecoration(
                          color: Colors.green[700],
                          borderRadius: BorderRadius.circular(2),
                        ),
                      ),
                  ],
                ),
              ),
            );
          },
        ),
      ),
      loading: () => const SizedBox(height: 50, child: Center(child: LinearProgressIndicator())),
      error: (e, s) => const SizedBox.shrink(),
    );
  }

  Widget _buildSummaryBar(List<TransactionModel> transactions, NumberFormat fmt) {
    double income = 0;
    double expense = 0;
    for (var t in transactions) {
      if (t.categoryFlux == 'Miditra' || t.categoryFlux == 'Vente') {
        income += t.totalAmountMga;
      } else if (t.categoryFlux == 'Fandaniana' || t.categoryFlux == 'Achat') {
        expense += t.totalAmountMga;
      }
    }
    final net = income - expense;

    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: const Color(0xFFE1F0F7),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          _buildSummaryItem(Icons.arrow_drop_down, Colors.red[700]!, '${fmt.format(expense)} Ar'),
          _buildSummaryItem(Icons.arrow_drop_up, Colors.green[700]!, '${fmt.format(income)} Ar'),
          Text(
            '= ${fmt.format(net)} Ar',
            style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
          ),
        ],
      ),
    );
  }

  Widget _buildSummaryItem(IconData icon, Color color, String amount) {
    return Row(
      children: [
        Icon(icon, color: color.withOpacity(0.6), size: 20),
        const SizedBox(width: 2),
        Text(
          amount.replaceAll(',', ' '),
          style: TextStyle(color: color, fontWeight: FontWeight.bold, fontSize: 13),
        ),
      ],
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

  static const _daysMg = {
    "Monday": "Alatsinainy", "Tuesday": "Talata", "Wednesday": "Alarobia",
    "Thursday": "Alakamisy", "Friday": "Zoma", "Saturday": "Sabotsy", "Sunday": "Alahady"
  };

  Widget _buildGroupedTransactionList(
    List<TransactionModel> transactions, 
    NumberFormat fmt, 
    Set<int> selectedIds, 
    bool isSelectionMode,
    WidgetRef ref
  ) {
    // Group transactions by date
    final Map<String, List<TransactionModel>> grouped = {};
    for (var t in transactions) {
      grouped.putIfAbsent(t.date, () => []).add(t);
    }

    final sortedDates = grouped.keys.toList()..sort((a, b) => b.compareTo(a));
    
    final List<dynamic> flatList = [];
    for (var date in sortedDates) {
      flatList.add(date); // Add date header
      flatList.addAll(grouped[date]!); // Add transactions for that date
    }

    return ListView.builder(
      padding: const EdgeInsets.only(bottom: 80),
      itemCount: flatList.length,
      itemBuilder: (context, index) {
        final item = flatList[index];

        if (item is String) {
          // Date Header
          final dateTransactions = grouped[item]!;
          double dayNet = 0;
          for (var t in dateTransactions) {
            final isExpense = t.categoryFlux == 'Fandaniana' || t.categoryFlux == 'Achat';
            dayNet += isExpense ? -t.totalAmountMga : t.totalAmountMga;
          }

          DateTime dt = DateTime.parse(item);
          String dayName = DateFormat('EEEE').format(dt);
          String mgDay = _daysMg[dayName] ?? dayName;
          String mgMonth = _monthsMg[dt.month]!.toLowerCase();
          String label = '$mgDay ${dt.day} $mgMonth ${dt.year}';

          return Padding(
            padding: const EdgeInsets.fromLTRB(16, 20, 16, 8),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(label, style: TextStyle(color: Colors.grey[600], fontSize: 13)),
                Text(
                  '${fmt.format(dayNet)} Ar'.replaceAll(',', ' '),
                  style: TextStyle(color: Colors.grey[700], fontSize: 13, fontWeight: FontWeight.w500),
                ),
              ],
            ),
          );
        }

        // Transaction Tile
        final t = item as TransactionModel;
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
          child: _buildTransactionTile(t, fmt, isSelected, isSelectionMode),
        );
      },
    );
  }

  Widget _buildTransactionTile(TransactionModel t, NumberFormat fmt, bool isSelected, bool isSelectionMode) {
    final isExpense = t.categoryFlux == 'Fandaniana' || t.categoryFlux == 'Achat';
    final color = isExpense ? Colors.red : Colors.green;
    
    IconData icon = Icons.shopping_bag;
    Color iconBg = Colors.orange[100]!;
    Color iconColor = Colors.orange[700]!;

    if (!isExpense) {
      icon = Icons.attach_money;
      iconBg = Colors.green[100]!;
      iconColor = Colors.green[700]!;
    }

    final itemLower = t.item.toLowerCase();
    if (itemLower.contains('bus') || itemLower.contains('taxi') || itemLower.contains('transport')) {
      icon = Icons.directions_bus;
      iconBg = Colors.blue[100]!;
      iconColor = Colors.blue[700]!;
    }

    return Container(
      color: isSelected ? color.withOpacity(0.05) : null,
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Row(
        children: [
          if (isSelectionMode)
            Padding(
              padding: const EdgeInsets.only(right: 12),
              child: Checkbox(
                value: isSelected, 
                onChanged: (val) {},
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(4)),
              ),
            )
          else
            Container(
              width: 44,
              height: 44,
              margin: const EdgeInsets.only(right: 12),
              decoration: BoxDecoration(
                color: iconBg,
                shape: BoxShape.circle,
              ),
              child: Icon(icon, color: iconColor, size: 24),
            ),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  t.item, 
                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                  overflow: TextOverflow.ellipsis,
                ),
                Text(
                  t.quantity != null && t.quantity! > 0
                    ? '${t.quantity} ${t.unit ?? ""}'
                    : t.providerClient ?? 'Divers',
                  style: TextStyle(fontSize: 12, color: Colors.grey[600]),
                ),
              ],
            ),
          ),
          Text(
            '${isExpense ? "-" : "+"}${fmt.format(t.totalAmountMga).replaceAll(',', ' ')} Ar',
            style: TextStyle(
              fontWeight: FontWeight.bold,
              color: isExpense ? Colors.red[500] : Colors.green[600],
              fontSize: 16,
            ),
          ),
        ],
      ),
    );
  }
}
