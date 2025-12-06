class Customer:
    def __init__(self, c_id: int, name: str, driver_license: str, email: str, phone: str):
        self.id = c_id
        self.name = name
        self.driver_license = driver_license  # Vital pour louer un véhicule
        self.email = email
        self.phone = phone

    def show_details(self):
        """Retourne une chaîne formatée pour l'affichage dans les menus/tableaux"""
        return f"[Client #{self.id}] {self.name} (Permis: {self.driver_license})"

    def to_dict(self):
        """Pour la sauvegarde JSON"""
        return {
            "id": self.id,
            "name": self.name,
            "driver_license": self.driver_license,
            "email": self.email,
            "phone": self.phone
        }

    # Cette méthode permettra de reconstruire l'objet depuis le dictionnaire JSON
    @staticmethod
    def from_dict(data):
        return Customer(
            data["id"],
            data["name"],
            data["driver_license"],
            data["email"],
            data["phone"]
        )