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
      content: SizedBox(
        width: double.maxFinite,
        child: SingleChildScrollView(
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
                InlineAutocompleteField(
                  suggestions: ref.watch(uniqueItemsProvider).value ?? const [],
                  controller: _itemController,
                  labelText: 'Zavatra (Item)',
                  validator: (value) => value == null || value.isEmpty ? 'Ilaina ity' : null,
                  onSelected: (value) {
                    _onItemChanged(value);
                  },
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
                    color: Theme.of(context).colorScheme.surfaceContainerHighest,
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
                InlineAutocompleteField(
                  suggestions: ref.watch(uniqueClientsProvider).value ?? const [],
                  controller: _clientController,
                  labelText: 'Mpandray / Mpamatsy',
                ),
              ],
            ),
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

/// A simple inline autocomplete field that shows suggestions below the text field.
/// Uses [addPostFrameCallback] to defer all focus-triggered state changes,
/// preventing layout-phase conflicts with AlertDialog's IntrinsicWidth.
class InlineAutocompleteField extends StatefulWidget {
  final List<String> suggestions;
  final TextEditingController controller;
  final String labelText;
  final FormFieldValidator<String>? validator;
  final ValueChanged<String>? onSelected;
  final TextInputType? keyboardType;

  const InlineAutocompleteField({
    super.key,
    required this.suggestions,
    required this.controller,
    required this.labelText,
    this.validator,
    this.onSelected,
    this.keyboardType,
  });

  @override
  State<InlineAutocompleteField> createState() => _InlineAutocompleteFieldState();
}

class _InlineAutocompleteFieldState extends State<InlineAutocompleteField> {
  final FocusNode _focusNode = FocusNode();
  List<String> _filteredSuggestions = [];
  bool _showSuggestions = false;

  @override
  void initState() {
    super.initState();
    _focusNode.addListener(_onFocusChanged);
  }

  /// Defers setState to after the current frame to avoid calling setState
  /// during a build/layout pass (which causes RenderIntrinsicWidth crashes).
  void _onFocusChanged() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (mounted) {
        if (_focusNode.hasFocus) {
          setState(() {
            _showSuggestions = true;
          });
        } else {
          // Delay hiding suggestions to allow onTap/onPressed to fire first.
          // This ensures clicks/taps on suggestions are registered on both Linux (mouse) and Android (tactile).
          Future.delayed(const Duration(milliseconds: 200), () {
            if (mounted && !_focusNode.hasFocus) {
              setState(() {
                _showSuggestions = false;
              });
            }
          });
        }
      }
    });
  }

  @override
  void dispose() {
    _focusNode.removeListener(_onFocusChanged);
    _focusNode.dispose();
    super.dispose();
  }

  void _onTextChanged(String text) {
    if (text.isEmpty) {
      if (mounted) {
        setState(() {
          _filteredSuggestions = [];
        });
      }
      return;
    }
    final filtered = widget.suggestions
        .where((s) => s.toLowerCase().contains(text.toLowerCase()) && s.toLowerCase() != text.toLowerCase())
        .toList();
    if (mounted) {
      setState(() {
        _filteredSuggestions = filtered;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final hasText = widget.controller.text.isNotEmpty;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisSize: MainAxisSize.min,
      children: [
        TextFormField(
          controller: widget.controller,
          focusNode: _focusNode,
          decoration: InputDecoration(
            labelText: widget.labelText,
            border: const OutlineInputBorder(),
            suffixIcon: hasText
                ? IconButton(
                    icon: const Icon(Icons.clear, size: 18),
                    onPressed: () {
                      widget.controller.clear();
                      widget.onSelected?.call('');
                      if (mounted) {
                        setState(() {
                          _filteredSuggestions = [];
                        });
                      }
                    },
                  )
                : null,
          ),
          validator: widget.validator,
          keyboardType: widget.keyboardType,
          onFieldSubmitted: (val) {
            widget.onSelected?.call(val);
            if (mounted) {
              setState(() {
                _showSuggestions = false;
              });
            }
          },
          onChanged: (val) {
            _onTextChanged(val);
            widget.onSelected?.call(val);
          },
        ),
        if (_showSuggestions) ...[
          if (widget.controller.text.isEmpty && widget.suggestions.isNotEmpty) ...[
            const SizedBox(height: 8),
            Text(
              'Soso-kevitra matetika :',
              style: TextStyle(
                fontSize: 12,
                color: Theme.of(context).colorScheme.primary,
                fontWeight: FontWeight.w600,
              ),
            ),
            const SizedBox(height: 4),
            SizedBox(
              height: 38,
              child: ListView.builder(
                scrollDirection: Axis.horizontal,
                itemCount: widget.suggestions.length > 8 ? 8 : widget.suggestions.length,
                itemBuilder: (context, index) {
                  final suggestion = widget.suggestions[index];
                  return Padding(
                    padding: const EdgeInsets.only(right: 6.0),
                    child: ActionChip(
                      label: Text(suggestion, style: const TextStyle(fontSize: 13)),
                      padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 0),
                      backgroundColor: Theme.of(context).colorScheme.surfaceContainerHighest,
                      onPressed: () {
                        widget.controller.text = suggestion;
                        widget.onSelected?.call(suggestion);
                        if (mounted) {
                          setState(() {
                            _showSuggestions = false;
                          });
                        }
                        _focusNode.unfocus();
                      },
                    ),
                  );
                },
              ),
            ),
          ] else if (_filteredSuggestions.isNotEmpty) ...[
            const SizedBox(height: 6),
            Container(
              constraints: const BoxConstraints(maxHeight: 140),
              decoration: BoxDecoration(
                color: Theme.of(context).colorScheme.surfaceContainerHighest,
                borderRadius: BorderRadius.circular(8),
                border: Border.all(color: Theme.of(context).colorScheme.outlineVariant),
              ),
              child: ClipRRect(
                borderRadius: BorderRadius.circular(8),
                child: ListView.builder(
                  shrinkWrap: true,
                  padding: EdgeInsets.zero,
                  itemCount: _filteredSuggestions.length,
                  itemBuilder: (context, index) {
                    final suggestion = _filteredSuggestions[index];
                    return ListTile(
                      title: Text(suggestion, style: const TextStyle(fontSize: 14)),
                      dense: true,
                      visualDensity: VisualDensity.compact,
                      onTap: () {
                        widget.controller.text = suggestion;
                        widget.onSelected?.call(suggestion);
                        if (mounted) {
                          setState(() {
                            _showSuggestions = false;
                            _filteredSuggestions = [];
                          });
                        }
                        _focusNode.unfocus();
                      },
                    );
                  },
                ),
              ),
            ),
          ],
        ],
      ],
    );
  }
}
