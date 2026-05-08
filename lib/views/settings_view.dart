import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:file_picker/file_picker.dart';
import '../services/database_helper.dart';
import '../providers/transaction_provider.dart';

class SettingsView extends ConsumerWidget {
  const SettingsView({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Fikirakirana'),
        centerTitle: true,
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _buildSectionHeader(context, 'Dataly (Données)'),
          ListTile(
            leading: const Icon(Icons.upload_file, color: Colors.blue),
            title: const Text('Hanafatra CSV (Importer CSV)'),
            subtitle: const Text('Ampidiro ny hara-mira avy amin\'ny fichier ivelany'),
            onTap: () => _importCsv(context, ref),
          ),
          ListTile(
            leading: const Icon(Icons.download, color: Colors.green),
            title: const Text('Handefa CSV (Exporter CSV)'),
            subtitle: const Text('Tehirizo ny hara-mira rehetra'),
            onTap: () => _exportCsv(context),
          ),
          const Divider(),
          _buildSectionHeader(context, 'Mombamomba (À propos)'),
          const ListTile(
            leading: Icon(Icons.info_outline),
            title: Text('CaisseCash'),
            subtitle: Text('Version 1.0.0 - Flutter Rewrite'),
          ),
        ],
      ),
    );
  }

  Widget _buildSectionHeader(BuildContext context, String title) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Text(
        title,
        style: TextStyle(
          color: Theme.of(context).colorScheme.primary,
          fontWeight: FontWeight.bold,
          fontSize: 14,
        ),
      ),
    );
  }

  Future<void> _importCsv(BuildContext context, WidgetRef ref) async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['csv'],
    );

    if (result != null && result.files.single.path != null) {
      try {
        final count = await DatabaseHelper.instance.importFromCsv(result.files.single.path!);
        ref.invalidate(transactionsProvider);
        ref.invalidate(summaryProvider);
        ref.invalidate(monthsProvider);
        
        if (context.mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('$count hara-mira voadika !'), backgroundColor: Colors.green),
          );
        }
      } catch (e) {
        if (context.mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Fahadisoana: $e'), backgroundColor: Colors.red),
          );
        }
      }
    }
  }

  Future<void> _exportCsv(BuildContext context) async {
    String? outputFile = await FilePicker.platform.saveFile(
      dialogTitle: 'Safidio ny toerana hitehirizana ny CSV',
      fileName: 'caissecash_export.csv',
      type: FileType.custom,
      allowedExtensions: ['csv'],
    );

    if (outputFile != null) {
      try {
        await DatabaseHelper.instance.exportToCsv(outputFile);
        if (context.mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Dataly voa-export tany amin\'ny: $outputFile'), backgroundColor: Colors.green),
          );
        }
      } catch (e) {
        if (context.mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Fahadisoana: $e'), backgroundColor: Colors.red),
          );
        }
      }
    }
  }
}
