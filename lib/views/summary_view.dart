import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../providers/transaction_provider.dart';
import '../widgets/evolution_chart.dart';
import '../widgets/distribution_chart.dart';

class SummaryView extends ConsumerWidget {
  const SummaryView({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final summaryAsync = ref.watch(summaryProvider);
    final numberFormat = NumberFormat("#,##0", "fr_FR");

    return Scaffold(
      appBar: AppBar(
        title: const Text('Témoin'),
        centerTitle: true,
      ),
      body: summaryAsync.when(
        data: (summary) {
          final balance = summary['balance'] ?? 0.0;
          final income = summary['income'] ?? 0.0;
          final expense = summary['expense'] ?? 0.0;

          return SingleChildScrollView(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                _buildBalanceCard(context, balance, numberFormat),
                const SizedBox(height: 20),
                Row(
                  children: [
                    Expanded(child: _buildStatCard(context, 'Miditra', income, Colors.green, Icons.arrow_downward, numberFormat)),
                    const SizedBox(width: 12),
                    Expanded(child: _buildStatCard(context, 'Fandaniana', expense, Colors.red, Icons.arrow_upward, numberFormat)),
                  ],
                ),
                const SizedBox(height: 24),
                _buildChartSection(context, 'Évolution du solde', const EvolutionChartWrapper()),
                const SizedBox(height: 24),
                _buildChartSection(context, 'Dépenses par item', const DistributionChartWrapper()),
              ],
            ),
          );
        },
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, stack) => Center(child: Text('Fahadisoana: $err')),
      ),
    );
  }

  Widget _buildChartSection(BuildContext context, String title, Widget chart) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.only(left: 8.0, bottom: 8.0),
          child: Text(title, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
        ),
        Card(
          elevation: 2,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: chart,
          ),
        ),
      ],
    );
  }

  Widget _buildBalanceCard(BuildContext context, double balance, NumberFormat fmt) {
    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      color: Theme.of(context).colorScheme.primaryContainer,
      child: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          children: [
            const Text('Solde Totaliny', style: TextStyle(fontSize: 16)),
            const SizedBox(height: 8),
            Text(
              '${fmt.format(balance).replaceAll(',', ' ')} Ar',
              style: TextStyle(
                fontSize: 32,
                fontWeight: FontWeight.bold,
                color: Theme.of(context).colorScheme.onPrimaryContainer,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStatCard(BuildContext context, String title, double amount, Color color, IconData icon, NumberFormat fmt) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(icon, size: 16, color: color),
                const SizedBox(width: 4),
                Text(title, style: const TextStyle(fontSize: 12)),
              ],
            ),
            const SizedBox(height: 8),
            Text(
              '${fmt.format(amount).replaceAll(',', ' ')}',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: color),
            ),
            const Text('Ar', style: TextStyle(fontSize: 10)),
          ],
        ),
      ),
    );
  }
}

class EvolutionChartWrapper extends ConsumerWidget {
  const EvolutionChartWrapper({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final evolutionAsync = ref.watch(evolutionProvider);
    return evolutionAsync.when(
      data: (data) => EvolutionChart(data: data),
      loading: () => const Center(child: CircularProgressIndicator()),
      error: (e, s) => Text('Erreur: $e'),
    );
  }
}

class DistributionChartWrapper extends ConsumerWidget {
  const DistributionChartWrapper({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final distributionAsync = ref.watch(distributionProvider);
    return distributionAsync.when(
      data: (data) => DistributionChart(data: data),
      loading: () => const Center(child: CircularProgressIndicator()),
      error: (e, s) => Text('Erreur: $e'),
    );
  }
}
