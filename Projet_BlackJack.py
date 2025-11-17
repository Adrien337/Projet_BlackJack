### Projet BlackJack ###
### Copyright © 2025. Tous droits réservés. ###

### Bibliothèques à importer ###

from tkinter import *
from tkinter import messagebox
from random import *

### Variables globales ###

root_width = 1250  # Largeur de la fenêtre
root_height = 750  # Hauteur de la fenêtre


### Classe Cartes ###

class Deck:
    def __init__(self):
        cartes_images = []
        for i in ["Coeur", "Carreau", "Pique", "Trefle"]:
            for j in ["As","2","3","4","5","6","7","8","9","10","Valet","Dame","Roi"]:
                img = PhotoImage(file=f"Images_cartes/{j}_{i}.png",name =f"{j}_{i}").subsample(6, 6)
                cartes_images.append(img)
        self.deck_cartes = cartes_images

    def melanger_deck(self, deck):
        shuffle(deck)

    def get_card_name(self,card):
        return card

### Classe BlackJack ###

class BlackJack: # 8 cartes max dans la main
    def __init__(self):
        self.cash = 200
        self.bet = 0
        self.quit_game = False
        self.cards = self.init_cards()

    def init_cards(self):
        # On initialise le paquet de cartes
        temp = []
        for symbol in ["Coeur", "Carreau", "Trefle", "Pique"]:
            for number_card in ["As", "2", "3", "4", "5", "6",  "7", "8", "9", "10", "Valet", "Dame", "Roi"]:
                temp.append([number_card, symbol])
        # On mélange les cartes
        lst_cards = []
        while len(temp) > 0:
            lst_cards.append(temp.pop(randint(0, len(temp) - 1)))
        return lst_cards

    def draw(self, lst_cards):
        return lst_cards.pop(0)

    def get_value_cards(self, lst_cards):
        total = 0
        temp = []
        for card in lst_cards:
            if card[0] == "As":
                # On met les As dans une liste temporaire pour s'en occuper plus tard
                temp.append(card)
            elif card[0] in ["Valet", "Dame", "Roi"]:
                total += 10
            else:
                total += int(card[0])

        # On s'occupe des As après pour pouvoir calculer la meilleure option
        for card in temp:
            as_value = 11
            if total + as_value <= 21:
                total += as_value
            else:
                total += 1
        return total

    def display_cards(self, player_type, player_cards, cards_value):
        print(f"{player_type} :", end=" ")
        for card in player_cards:
            if card[1] == "Coeur":
                card[1] = "♥"
            elif card[1] == "Carreau":
                card[1] = "♦"
            elif card[1] == "Trefle":
                card[1] = "♣"
            else:
                card[1] = "♠"
            print(f"{card[0]}{card[1]}", end=" ")
        print(f"({cards_value})")

    def to_bet(self, money_left):
        mise_minimum = 20
        if money_left < mise_minimum:
            return False
        money_bet = "NaN"
        can_continue = False
        while can_continue != True:
            money_bet = input("Combien d'argent voulez vous parier ? ")
            if money_bet.isdigit() == True:
                money_bet = int(money_bet)
                if money_bet > money_left:
                    print(
                        "Oups !\nIl semblerait que vous n'ayez pas assez d'argent...\nMerci de rentrer une mise plus petite."
                    )
                    money_bet = "NaN"
                elif money_bet < mise_minimum:
                    print("La mise minimum requise est de 20$")
                    money_bet = "NaN"
                else:
                    can_continue = True
            else:
                print("Vous n'avez pas entré d'entiers !\nVeuillez réessayer")
        self.cash -= int(money_bet)
        print(f"Argent restant = {self.cash}; argent parié : {money_bet}")
        return money_bet


### Création du menu ###


def Creer_menu_principal(root):
    def Effacer_menu_principal():
        for widget in root.winfo_children():
            widget.destroy()

    root.title("Projet BlackJack - Menu principal")
    # Fond de couleur plus sombre et titre centré
    titre = Label(
        root, text="BLACKJACK", font=("Helvetica", 64, "bold"), fg="white", bg="#202020"
    )
    titre.place(relx=0.5, rely=0.25, anchor="center")

    # Création d'un bouton stylé
    bouton_jouer = Button(
        root,
        text="JOUER",
        font=("Helvetica", 24, "bold"),
        bg="#4CAF50",
        fg="white",
        activebackground="#66BB6A",
        activeforeground="white",
        relief="flat",
        width=15,
        height=2,
        bd=0,
        cursor="hand2",
        command = lambda:(Effacer_menu_principal(),Lancer_jeu(root))
    )
    bouton_jouer.place(relx=0.5, rely=0.5, anchor="center")

    # Effet de survol (hover)
    def on_enter(e):
        bouton_jouer.config(bg="#66BB6A")

    def on_leave(e):
        bouton_jouer.config(bg="#4CAF50")

    bouton_jouer.bind("<Enter>", on_enter)
    bouton_jouer.bind("<Leave>", on_leave)

    # Bouton Quitter
    bouton_quitter = Button(
        root,
        text="Quitter",
        font=("Helvetica", 16, "bold"),
        bg="#C62828",
        fg="white",
        activebackground="#E53935",
        relief="flat",
        width=10,
        height=1,
        bd=0,
        cursor="hand2",
        command=root.quit,
    )
    bouton_quitter.place(relx=0.5, rely=0.65, anchor="center")

    # Fond général
    root.configure(bg="#202020")

def Lancer_jeu(root):
    def Effacer_jeu(root):
        """Efface tous les widgets de l'écran de jeu avant de revenir au menu"""
        for widget in root.winfo_children():
            widget.destroy()

    # --- On crée une instance réelle de la classe BlackJack ---
    game = BlackJack()

    root.title("Projet BlackJack - Jeu")
    root.configure(bg="#1E1E1E")

    # --- Label lié à la variable d’argent du joueur ---
    argent_label_var = StringVar()
    argent_label_var.set(f"Argent restant : {game.cash} $")

    label_argent = Label(
        root,
        textvariable=argent_label_var,
        font=("Helvetica", 24, "bold"),
        fg="#FFD700",
        bg="#1E1E1E"
    )
    label_argent.place(relx=0.5, rely=0.1, anchor="center")

    # --- Bouton pour revenir au menu ---
    bouton_retour = Button(
        root,
        text="← Retour au menu",
        font=("Helvetica", 14, "bold"),
        bg="#424242",
        fg="white",
        activebackground="#616161",
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        command=lambda: (Effacer_jeu(root), Creer_menu_principal(root))
    )
    bouton_retour.place(x=20, y=20)

    # --- Zone de plateau pour les cartes (future zone de jeu) ---
    plateau = Frame(root, bg="#2C2C2C", width=1000, height=400)
    plateau.place(relx=0.5, rely=0.55, anchor="center")

    # --- Exemple de bouton : déduire une mise ---
    def parier_20():
        if game.cash >= 20:
            game.cash -= 20
            argent_label_var.set(f"Argent restant : {game.cash} $")
        else:
            messagebox.showinfo("Plus d'argent", "Vous n'avez plus assez d'argent pour parier !")

    bouton_parier = Button(
        root,
        text="Parier 20$ (test)",
        font=("Helvetica", 14, "bold"),
        bg="#4CAF50",
        fg="white",
        activebackground="#66BB6A",
        relief="flat",
        bd=0,
        cursor="hand2",
        command=parier_20
    )
    bouton_parier.place(relx=0.5, rely=0.85, anchor="center")

    # --- Exemple de bouton : gagner de l’argent ---
    def gagner_20():
        game.cash += 20
        argent_label_var.set(f"Argent restant : {game.cash} $")

    bouton_gagner = Button(
        root,
        text="Gagner 20$ (test)",
        font=("Helvetica", 14, "bold"),
        bg="#1E88E5",
        fg="white",
        activebackground="#42A5F5",
        relief="flat",
        bd=0,
        cursor="hand2",
        command=gagner_20
    )
    bouton_gagner.place(relx=0.5, rely=0.9, anchor="center")


### Configuration de la fenêtre ###

root = Tk()
root.resizable(False, False)
root.geometry(f"{root_width}x{root_height}")
root.configure(background="#808080")

### On gère les évènements ###

deck = Deck()
print(deck.get_card_name(deck[0]))
Creer_menu_principal(root)

root.mainloop()

quit()

### Variables globales ###




game = BlackJack()
while game.quit_game == False:
    print(f"Votre argent : {game.cash}$")
    game.bet = game.to_bet(game.cash)
    if game.bet == False:  # On vérifie si le joueur à assez d'argent
        print("Vous n'avez pas assez d'argent pour jouer !")
        break

    print()  # Pour sauter des lignes dans le terminal
    Croupier = []
    Croupier.append(game.draw(game.cards))  # On fait piocher une carte
    game.display_cards(
        "Croupier", Croupier, game.get_value_cards(Croupier)
    )  # On affiche les cartes

    Joueur = []
    Joueur.append(game.draw(game.cards))  # On fait piocher une carte
    game.display_cards(
        "Joueur", Joueur, game.get_value_cards(Joueur)
    )  # On affiche les cartes

    print()  # Pour sauter des lignes dans le terminal
    Continue_draw = True
    while Continue_draw != False:
        if game.get_value_cards(Joueur) > 21:  # Si on dépasse les 21
            print("Perdu !\n Vous avez dépassé 21.")
            break
        print()  # Pour sauter des lignes dans le terminal
        Continue_draw = (
            input("Continuer à piocher ? (y/n): ").lower().startswith("y")
        )  # True si la réponse commence par y, False sinon
        if Continue_draw:
            Joueur.append(game.draw(game.cards))  # On fait piocher une carte
            game.display_cards(
                "Joueur", Joueur, game.get_value_cards(Joueur)
            )  # On affiche les cartes

    print()  # Pour sauter des lignes dans le terminal
    game.display_cards(
        "Croupier", Croupier, game.get_value_cards(Croupier)
    )  # On affiche les cartes
    game.display_cards(
        "Joueur", Joueur, game.get_value_cards(Joueur)
    )  # On affiche les cartes

    print()  # Pour sauter des lignes dans le terminal
    can_continue = (
        True if game.get_value_cards(Joueur) <= 21 else False
    )  # Si le joueur à déjà perdu, pas la peine de piocher
    while can_continue:
        Croupier.append(game.draw(game.cards))  # On fait piocher une carte
        if game.get_value_cards(Croupier) > 21:  # Si le croupier dépasse les 21
            game.display_cards(
                "Croupier", Croupier, game.get_value_cards(Croupier)
            )  # On affiche les cartes
            print(f"Le croupier à perdu ! Vous gagnez {game.bet*2}$")
            game.cash += game.bet * 2
            break
        elif game.get_value_cards(Croupier) == game.get_value_cards(
            Joueur
        ):  # Si il y a égalité
            game.display_cards(
                "Croupier", Croupier, game.get_value_cards(Croupier)
            )  # On affiche les cartes
            print(f"Egalité ! Vous reprenez votre mise de {game.bet}")
            game.cash += game.bet
            break
        elif game.get_value_cards(Croupier) > game.get_value_cards(
            Joueur
        ):  # Si le croupier nous bat
            game.display_cards(
                "Croupier", Croupier, game.get_value_cards(Croupier)
            )  # On affiche les cartes
            print(
                f"Le croupier à une meilleure main que vous ! Vous perdez votre mise de {game.bet}"
            )
            break

    print()  # Pour sauter des lignes dans le terminal
    Continue_game = (
        input("Continuer à jouer ? (y/n): ").lower().startswith("y")
    )  # True si la réponse commence par y, False sinon
    if not Continue_game:  # Si on veut quitter, on quitte
        game.quit_game = True
print("Merci d'avoir parié votre argent et toute votre vie chez nous !")
