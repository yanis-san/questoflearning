from django.db import models
from django.core.exceptions import ObjectDoesNotExist

"""
Détails du Fonctionnement
Initialisation (__init__) :

Le champ peut être initialisé avec un paramètre for_fields qui indique les champs à utiliser pour filtrer et organiser les objets.
Méthode pre_save :

Avant de sauvegarder un nouvel objet, cette méthode vérifie si une valeur d’ordre est déjà définie.
Si non, elle cherche le plus grand numéro d’ordre parmi les objets existants et assigne le suivant (par exemple, si les objets existants ont des ordres 1, 2, et 3, le nouvel objet recevra 4).
Si aucun objet n’existe encore, il assigne l’ordre 0.
En Résumé
Ordre des Objets : Permet de contrôler la manière dont les objets sont triés et affichés.
Champ OrderField : Automatise l’attribution des valeurs d’ordre et assure que les objets sont correctement triés en fonction des valeurs d’ordre spécifiées.
"""


class OrderField(models.PositiveIntegerField):
    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            # Pas encore de valeur pour ce champ
            try:
                qs = self.model.objects.all()
                if self.for_fields:
                    # Filtrer par les valeurs des champs spécifiés dans for_fields
                    query = {field: getattr(model_instance, field) for field in self.for_fields}
                    qs = qs.filter(**query)
                # Obtenir l'ordre du dernier élément
                last_item = qs.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)