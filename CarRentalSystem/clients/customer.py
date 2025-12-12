class Customer:
    def __init__(self, c_id: int, name: str, driver_license: str, email: str, phone: str, username: str, password: str):
        self.id = c_id
        self.name = name
        self.driver_license = driver_license
        self.email = email
        self.phone = phone
        self.username = username # Nouveau
        self.password = password

    def show_details(self):
        return f"[Client #{self.id}] {self.name} (Permis: {self.driver_license})"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "driver_license": self.driver_license,
            "email": self.email,
            "phone": self.phone,
            "username": self.username, # Sauvegarde
            "password": self.password  # Sauvegarde
        }
    
    def to_table_row(self):
        return {
            "ID": self.id,
            "Nom": self.name,
            "Utilisateur": self.username,
            "Permis": self.driver_license,
            "Email": self.email
        }