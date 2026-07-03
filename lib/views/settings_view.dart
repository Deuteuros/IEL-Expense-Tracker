import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:file_picker/file_picker.dart';
import 'package:share_plus/share_plus.dart';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' as p;
import '../services/database_helper.dart';
import '../providers/transaction_provider.dart';
import '../providers/web_socket_provider.dart';

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
          _buildSectionHeader(context, 'Tambazotra (Réseau Local)'),
          Consumer(
            builder: (context, ref, child) {
              final wsManager = ref.watch(webSocketServerProvider);
              return Card(
                elevation: 0,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                  side: BorderSide(color: Colors.grey.shade300),
                ),
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(
                            wsManager.isRunning ? 'Mandeha ny serveur (Actif)' : 'Mijanona ny serveur (Inactif)',
                            style: TextStyle(
                              fontWeight: FontWeight.bold,
                              color: wsManager.isRunning ? Colors.green : Colors.red,
                            ),
                          ),
                          Switch(
                            value: wsManager.isRunning,
                            onChanged: (value) {
                              if (value) {
                                wsManager.start();
                              } else {
                                wsManager.stop();
                              }
                            },
                          ),
                        ],
                      ),
                      if (wsManager.isRunning) ...[
                        const SizedBox(height: 8),
                        SelectableText(
                          'Adiresy IP: ws://${wsManager.ipAddress}:${wsManager.port}/ws',
                          style: const TextStyle(fontFamily: 'monospace', fontSize: 13, fontWeight: FontWeight.w600),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          'Mpanjifa mifandray (Clients): ${wsManager.connectedClientsCount}',
                          style: TextStyle(color: Colors.grey.shade700),
                        ),
                      ],
                    ],
                  ),
                ),
              );
            },
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
        ref.invalidate(evolutionProvider);
        ref.invalidate(distributionProvider);
        
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
    if (Platform.isAndroid || Platform.isIOS) {
      try {
        final tempDir = await getTemporaryDirectory();
        final tempPath = p.join(tempDir.path, 'caissecash_export.csv');
        
        await DatabaseHelper.instance.exportToCsv(tempPath);
        
        await Share.shareXFiles(
          [XFile(tempPath)],
          subject: 'Export CaisseCash CSV',
          text: 'Ireto ny dataly avy amin\'ny CaisseCash.',
        );
      } catch (e) {
        if (context.mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Fahadisoana: $e'), backgroundColor: Colors.red),
          );
        }
      }
    } else {
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
}
