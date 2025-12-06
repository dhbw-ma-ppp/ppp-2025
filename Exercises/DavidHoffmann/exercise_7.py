import pandas as pd
import numpy as np
import os

# Aufgabenstellung:
# Vorgegeben ist eine Block aus Zahlen. 
# Jede Zahl gibt dabei einen möglichen Weg für
# ein U-Boot in einer Höhle wieder. Man startet oben links im 
# Nummernblock und will nach unten rechts(Ausgang der Höhle).
# Die Zahlen geben dabei nicht nur einen möglichen Weg an
# sondern auch das Risiko, dass das U-Boot gegen Chitons
# an der Höhlenwand kracht, sollte dieser Weg genommen werden.
# Das Ziel ist zum Ausgang der Höhle(unten rechts im Block) zu kommen und
# dabei den Weg mit dem niedrigsten Risiko zu wählen.


class Ubootnavigation():
    
    def __init__(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "exercise_cave.txt")
        numbers = pd.read_csv(file_path, header=None, dtype=str)
        #verkompliziertes pd.read("exercise_cave.txt"), hat sonst keinen Nutzen
        raw_column = numbers.iloc[:, 0]
        list_of_lists = [[int(digit) for digit in row] for row in raw_column]
        # in self.karte wird ein zwei diminsionales array mit den risk-Werten aus excercise_cave gespeichert.
        self.karte = np.array(list_of_lists)

        rows = len(self.karte)
        columns = len(self.karte[0])
        
        self.pos_x = 0
        self.pos_y = 0
        self.position_coords = (self.pos_x,self.pos_y)
        self.goal_pos_x = len(self.karte[0]) - 1
        self.goal_pos_y = len(self.karte) - 1
        self.goal_posistion_coords = (self.goal_pos_x,self.goal_pos_y)
        self.unchecked_knots = {}
        self.checked_knots = {}

    def get_neighbours(self):
        current_neigbours = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for (direc_x, direc_y) in directions:
            coords = (self.pos_x + direc_x, self.pos_y + direc_y)
            
            # überprüfung ob der jewilige Nachbar berites besucht wurde
            if (coords) in self.checked_knots:
                continue 
                # überprüfung ob der jewilige nachbar innerhalb des Feldes ist
            else:
                if 0 <= coords[0] < len(self.karte) and 0 <= coords[1] < len(self.karte[0]):     
                    current_neigbours.append(coords)

        return current_neigbours
        

    def get_best_route(self):
        # Ich nutze den A*-Algorythmus, um den günstigsten Weg zu finden.
        # Er ähnelt dem Dijkstra-Algorythmus stark, hat aber einen entscheidenden Unterschied.
        # Der A*-Algorythmus nutzt zwei Werte, um zu bestimmen, welcher Weg am sinnvollsten ist, um
        # möglichst günstig zum Ziel zu kommen.
        # 1. Tatsächlichen Kosten g(n):
        # Die SUmme der Kosten vom Startknoten zum aktuellen Knoten
        # 2. geschätzte Kosten bis zum Ziel h(n)
        # Dafür gibt es verschiedene Methoden. Ich berechne sie hier mit der Mannhatten-Methode 
        #|x_ziel - x_knoten| + |y_ziel - y_knoten|
        # 
        # Diese beiden Werte werden addiert. Der Knoten mit den niedrigsten Totalen Kosten f(n), wird
        # als nächster Knoten ausgewählt
        # 
        # current_risk = g(n)
        # current_estimated_risk = h(n)
        # total_cost = f(n) = g(n) + h(n)

        # ich füge die Startposition, in das uncheckend Dictionary ein,
        # setze allerdings alle Daten auf 0, da die Daten des Startpunkts nicht in 
        # die Berechnung einfließen sollen
        self.unchecked_knots[self.position_coords] = {
            "current_risk" : 0,
            "current_estimated_risk_to_reach_goal" : 0,
            "total_cost" : 0
        }
        while 1:
            knot_with_lowest_total_cost = min(
                self.unchecked_knots, 
                key=lambda coords: self.unchecked_knots[coords]["total_cost"]
            )
            # hier hole ich mir aus dem unchecked Dict die Koordinaten mit dem niedrigsten total_cost wert heraus.
            self.position_coords = knot_with_lowest_total_cost
            self.pos_x = self.position_coords[0]
            self.pos_y = self.position_coords[1]
            # hier setze ich die Position des Uboots auf die oben geholten Koordinaten

            if knot_with_lowest_total_cost == self.goal_posistion_coords:
                gesamt_risiko = self.unchecked_knots[knot_with_lowest_total_cost]["current_risk"]
                print("Top, wir haben es geschafft")
                print(f"Das Gesamtrisiko, für den vorgeschlagenen Weg ist : {gesamt_risiko}")
                # hier wird überprüft, ob die Koordinaten mit den Ziel Koordnaten übereinstimmen
                # und dann gegebenenfalls die Schleife abgfebrochen
                # Vorher hole ich mir noch das current_risk. Darin ist bereits das Risiko, von allen gewählten Knoten aufsummiert.
                break
            else:
                current_neigbours = self.get_neighbours()
                for neighbour in current_neigbours:

                    current_risk = self.karte[neighbour[0]][neighbour[1]] + self.unchecked_knots[knot_with_lowest_total_cost]["current_risk"]
                    current_estimated_cost_to_goal = abs(self.goal_pos_x - neighbour[0]) + abs(self.goal_pos_y - neighbour[1])
                    total_cost = current_risk + current_estimated_cost_to_goal
                    # hier werden alle wichtigen Informationen über die Nachbarn des aktuellen Knotens berechnet
                    if neighbour in self.unchecked_knots and self.unchecked_knots[neighbour]["current_risk"] > current_risk:
                        self.unchecked_knots[neighbour] = {
                            "current_risk" : current_risk,
                            "current_estimated_risk_to_reach_goal" : current_estimated_cost_to_goal,
                            "total_cost" : total_cost
                        }
                        continue
                    # Die Daten werden nur überschrieben, wenn die vorherigen Daten schlechter waren
                    if neighbour not in self.unchecked_knots:
                        self.unchecked_knots[neighbour] = {
                            "current_risk" : current_risk,
                            "current_estimated_risk_to_reach_goal" : current_estimated_cost_to_goal,
                            "total_cost" : total_cost
                        }

                    # die Daten werden nur eingefügt, wenn der Knoten nicht breits im Dictionary vorhanden sind
                data = self.unchecked_knots[knot_with_lowest_total_cost]
                self.checked_knots[knot_with_lowest_total_cost] = data
                del self.unchecked_knots[knot_with_lowest_total_cost]
                # hier wird der günstigste Knoten aus dem unchecked dictionary gelöscht und in das checked dictionary eingefügt,
                # damit der Knoten nicht nochmal als günstigster knoten ausgewählt werden kann und nicht nochmal als möglicher Nachbar
                # angenommen werden kann(Das U-Boot soll keine Schleifen fahren)

Uboot = Ubootnavigation()
Uboot.get_best_route()