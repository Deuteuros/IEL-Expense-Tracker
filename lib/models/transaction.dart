class TransactionModel {
  final int? id;
  final String date; // YYYY-MM-DD
  final String categoryFlux; // Miditra, Fandaniana, etc.
  final String item;
  final double? quantity;
  final String? unit;
  final double? unitPrice;
  final double totalAmountMga;
  final String? providerClient;
  final int? walletId;

  TransactionModel({
    this.id,
    required this.date,
    required this.categoryFlux,
    required this.item,
    this.quantity,
    this.unit,
    this.unitPrice,
    required this.totalAmountMga,
    this.providerClient,
    this.walletId,
  });

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'date': date,
      'categorie_flux': categoryFlux,
      'item': item,
      'quantite': quantity,
      'unite': unit,
      'prix_unitaire': unitPrice,
      'montant_total_mga': totalAmountMga,
      'fournisseur_client': providerClient,
      'portefeuille_id': walletId,
    };
  }

  factory TransactionModel.fromMap(Map<String, dynamic> map) {
    return TransactionModel(
      id: map['id'],
      date: map['date'],
      categoryFlux: map['categorie_flux'],
      item: map['item'],
      quantity: map['quantite'],
      unit: map['unite'],
      unitPrice: map['prix_unitaire'],
      totalAmountMga: map['montant_total_mga'],
      providerClient: map['fournisseur_client'],
      walletId: map['portefeuille_id'],
    );
  }
}
