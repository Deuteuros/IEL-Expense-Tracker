import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'summary_view.dart';
import 'history_view.dart';
import 'settings_view.dart';
import '../widgets/add_transaction_dialog.dart';
import '../providers/transaction_provider.dart';

final navigationIndexProvider = StateProvider<int>((ref) => 0);

class MainScreen extends ConsumerWidget {
  const MainScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final selectedIndex = ref.watch(navigationIndexProvider);

    final List<Widget> views = [
      const SummaryView(),
      const HistoryView(),
      const SettingsView(),
    ];

    return Scaffold(
      body: IndexedStack(
        index: selectedIndex,
        children: views,
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: selectedIndex,
        onDestinationSelected: (index) {
          ref.read(navigationIndexProvider.notifier).state = index;
        },
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.dashboard_outlined),
            selectedIcon: Icon(Icons.dashboard),
            label: 'Témoin',
          ),
          NavigationDestination(
            icon: Icon(Icons.history_outlined),
            selectedIcon: Icon(Icons.history),
            label: 'Tantara',
          ),
          NavigationDestination(
            icon: Icon(Icons.settings_outlined),
            selectedIcon: Icon(Icons.settings),
            label: 'Fikirakirana',
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          showDialog(
            context: context,
            builder: (context) => AddTransactionDialog(
              onSaved: () {
                ref.invalidate(transactionsProvider);
                ref.invalidate(summaryProvider);
                ref.invalidate(monthsProvider);
                ref.invalidate(evolutionProvider);
                ref.invalidate(distributionProvider);
              },
            ),
          );
        },
        backgroundColor: Theme.of(context).colorScheme.primaryContainer,
        child: const Icon(Icons.add),
      ),
    );
  }
}
