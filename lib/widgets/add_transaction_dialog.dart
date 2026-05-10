import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/transaction.dart';
import '../services/database_helper.dart';
import '../providers/transaction_provider.dart';

class AddTransactionDialog extends ConsumerStatefulWidget {
  final VoidCallback onSaved;

  const AddTransactionDialog({super.key, required this.onSaved});

  @override
  ConsumerState<AddTransactionDialog> createState() => _AddTransactionDialogState();
}

class _AddTransactionDialogState extends ConsumerState<AddTransactionDialog> {
  final _formKey = GlobalKey<FormState>();
  
  String _categoryFlux = 'Fandaniana'; // Default
  final _itemController = TextEditingController();
  final _qtyController = TextEditingController();
  final _unitController = TextEditingController();
  final _priceController = TextEditingController();
  final _clientController = TextEditingController();
  
  double _total = 0.0;
  final _numberFormat = NumberFormat("#,##0", "fr_FR");

  void _calculateTotal() {
    final qty = double.tryParse(_qtyController.text) ?? 0.0;
    final price = double.tryParse(_priceController.text) ?? 0.0;
    setState(() {
      _total = qty * price;
    });
  }

  Future<void> _onItemChanged(String item) async {
    if (item.isEmpty) return;
    final unit = await DatabaseHelper.instance.getRecentUnitForItem(item);
    if (unit != null && unit.isNotEmpty && mounted) {
      setState(() {
        _unitController.text = unit;
      });
    }
  }

  @override
  void initState() {
    super.initState();
    _qtyController.addListener(_calculateTotal);
    _priceController.addListener(_calculateTotal);
  }

  @override
  void dispose() {
    _itemController.dispose();
    _qtyController.dispose();
    _unitController.dispose();
    _priceController.dispose();
    _clientController.dispose();
    super.dispose();
  }

  Future<void> _save() async {
    if (_formKey.currentState!.validate()) {
      final transaction = TransactionModel(
        date: DateFormat('yyyy-MM-dd').format(DateTime.now()),
        categoryFlux: _categoryFlux,
        item: _itemController.text,
        quantity: double.tryParse(_qtyController.text),
        unit: _unitController.text,
        unitPrice: double.tryParse(_priceController.text),
        totalAmountMga: _total,
        providerClient: _clientController.text,
        walletId: 1, // Default Caisse
      );

      await DatabaseHelper.instance.insertTransaction(transaction);
      widget.onSaved();
      if (mounted) Navigator.of(context).pop();
    }
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('Ampidiro fandaniana / miditra', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
      content: SingleChildScrollView(
        child: Form(
          key: _formKey,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              SegmentedButton<String>(
                segments: const [
                  ButtonSegment(value: 'Miditra', label: Text('Miditra'), icon: Icon(Icons.add)),
                  ButtonSegment(value: 'Fandaniana', label: Text('Fandaniana'), icon: Icon(Icons.remove)),
                ],
                selected: {_categoryFlux},
                onSelectionChanged: (Set<String> newSelection) {
                  setState(() {
                    _categoryFlux = newSelection.first;
                  });
                },
              ),
              const SizedBox(height: 16),
              // Item Autocomplete
              ref.watch(uniqueItemsProvider).when(
                data: (items) => Autocomplete<String>(
                  initialValue: TextEditingValue(text: _itemController.text),
                  optionsBuilder: (TextEditingValue textEditingValue) {
                    if (textEditingValue.text == '') return const Iterable<String>.empty();
                    return items.where((String option) => option.toLowerCase().contains(textEditingValue.text.toLowerCase()));
                  },
                  onSelected: (String selection) {
                    _itemController.text = selection;
                    _onItemChanged(selection);
                  },
                  fieldViewBuilder: (context, controller, focusNode, onFieldSubmitted) {
                    // Sync controller
                    if (controller.text != _itemController.text && _itemController.text.isNotEmpty && controller.text.isEmpty) {
                       controller.text = _itemController.text;
                    }
                    return TextFormField(
                      controller: controller,
                      focusNode: focusNode,
                      decoration: const InputDecoration(labelText: 'Zavatra (Item)', border: OutlineInputBorder()),
                      validator: (value) => value == null || value.isEmpty ? 'Ilaina ity' : null,
                      onChanged: (value) {
                        _itemController.text = value;
                      },
                      onFieldSubmitted: (value) {
                        onFieldSubmitted();
                        _onItemChanged(value);
                      },
                    );
                  },
                ),
                loading: () => const LinearProgressIndicator(),
                error: (_, __) => TextFormField(
                  controller: _itemController,
                  decoration: const InputDecoration(labelText: 'Zavatra (Item)', border: OutlineInputBorder()),
                  validator: (value) => value == null || value.isEmpty ? 'Ilaina ity' : null,
                ),
              ),
              const SizedBox(height: 10),
              Row(
                children: [
                  Expanded(
                    child: TextFormField(
                      controller: _qtyController,
                      decoration: const InputDecoration(labelText: 'Isa (Quantité)', border: OutlineInputBorder()),
                      keyboardType: TextInputType.number,
                      validator: (value) => value == null || value.isEmpty ? 'Ilaina' : null,
                    ),
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: TextFormField(
                      controller: _unitController,
                      decoration: const InputDecoration(labelText: 'Singa (Unité)', border: OutlineInputBorder()),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 10),
              TextFormField(
                controller: _priceController,
                decoration: const InputDecoration(labelText: 'Vidy isany (Prix unitaire)', border: OutlineInputBorder(), suffixText: 'Ar'),
                keyboardType: TextInputType.number,
                validator: (value) => value == null || value.isEmpty ? 'Ilaina' : null,
              ),
              const SizedBox(height: 16),
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Theme.of(context).colorScheme.surfaceVariant,
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text('Totaliny :', style: TextStyle(fontWeight: FontWeight.bold)),
                    Text('${_numberFormat.format(_total).replaceAll(',', ' ')} Ar', 
                      style: TextStyle(fontWeight: FontWeight.bold, color: Theme.of(context).colorScheme.primary, fontSize: 18)),
                  ],
                ),
              ),
              const SizedBox(height: 10),
              // Client Autocomplete
              ref.watch(uniqueClientsProvider).when(
                data: (clients) => Autocomplete<String>(
                  initialValue: TextEditingValue(text: _clientController.text),
                  optionsBuilder: (TextEditingValue textEditingValue) {
                    if (textEditingValue.text == '') return const Iterable<String>.empty();
                    return clients.where((String option) => option.toLowerCase().contains(textEditingValue.text.toLowerCase()));
                  },
                  onSelected: (String selection) {
                    _clientController.text = selection;
                  },
                  fieldViewBuilder: (context, controller, focusNode, onFieldSubmitted) {
                    if (controller.text != _clientController.text && _clientController.text.isNotEmpty && controller.text.isEmpty) {
                       controller.text = _clientController.text;
                    }
                    return TextFormField(
                      controller: controller,
                      focusNode: focusNode,
                      decoration: const InputDecoration(labelText: 'Mpandray / Mpamatsy', border: OutlineInputBorder()),
                      onChanged: (value) {
                        _clientController.text = value;
                      },
                    );
                  },
                ),
                loading: () => const SizedBox(height: 2, child: LinearProgressIndicator()),
                error: (_, __) => TextFormField(
                  controller: _clientController,
                  decoration: const InputDecoration(labelText: 'Mpandray / Mpamatsy', border: OutlineInputBorder()),
                ),
              ),
            ],
          ),
        ),
      ),
      actions: [
        TextButton(onPressed: () => Navigator.pop(context), child: const Text('Hanafoana')),
        FilledButton(onPressed: _save, child: const Text('Ampidiro')),
      ],
    );
  }
}
