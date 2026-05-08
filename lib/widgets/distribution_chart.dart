import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';

class DistributionChart extends StatelessWidget {
  final List<Map<String, dynamic>> data;

  const DistributionChart({super.key, required this.data});

  @override
  Widget build(BuildContext context) {
    if (data.isEmpty) {
      return const SizedBox(
        height: 200,
        child: Center(child: Text('Tsy misy fandaniana (Aucune dépense)')),
      );
    }

    final List<Color> colors = [
      Colors.blue,
      Colors.red,
      Colors.orange,
      Colors.green,
      Colors.purple,
    ];

    return SizedBox(
      height: 200,
      child: PieChart(
        PieChartData(
          sectionsSpace: 2,
          centerSpaceRadius: 40,
          sections: data.asMap().entries.map((e) {
            final index = e.key;
            final item = e.value['item'] as String;
            final total = (e.value['total'] as num).toDouble();
            
            return PieChartSectionData(
              color: colors[index % colors.length],
              value: total,
              title: item,
              radius: 50,
              titleStyle: const TextStyle(
                fontSize: 10,
                fontWeight: FontWeight.bold,
                color: Colors.white,
              ),
            );
          }).toList(),
        ),
      ),
    );
  }
}
