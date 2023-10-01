import sys 
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D

class AirflowSimulator(QMainWindow):
    def __init__(self, grid_size=(10, 10), time_steps=100):
        super().__init__()

        self.grid_size = grid_size
        self.time_step = time_steps
        self.airflow_grid = np.zeros(grid_size)

        # Initialisation des propriétés de la fenêtre 
        self.setWindowTitle("Airflow Simulator")
        self.setGeometry(100, 100, 800,600) # Initialisation de la taille et la position de la fenêtre

        # Création d'un widget central
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Création d'un conteneur pour le widget central
        layout = QVBoxLayout(central_widget)

        # Création d'un label
        label = QLabel("Bienvenue dans le simulateur d'air", self)
        layout.addWidget(label)

        # Création d'un bouton
        simulate_button = QPushButton("Simuler", self)
        simulate_button.resize(150, 50)
        simulate_button.clicked.connect(self.start_simulation)
        layout.addWidget(simulate_button)

        # Création d'un graph 
        self.figure = plt.figure(figsize=(16, 12))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    def initialize_simulation(self):
        # Initialisation de la grille de l'écoulement avec les conditions initiales
        # Pour simplifier, on commence avec un champ d"écoulement uniforme  
        self.airflow_grid = np.ones(self.grid_size)

    def run_simulation(self):
        for step in range(self.time_step):
            # Effectue un pas de temps dans la simulation
            self.advection_diffusion_step()
            self.update_plot()

    def advection_diffusion_step(self):
        # Simulation du transport de la quantité d'air et de la diffusion
        advection_rate = 0.1
        diffusion_rate = 0.01
        new_airflow_grid = np.zeros(self.grid_size)

        for i in range(1, self.grid_size[0] - 1):
            for j in range (1, self.grid_size[1] - 1):
                # Terme de l'advection de l'air (transport de la quantité d'air) 
                advected_value = self.airflow_grid[i, j] - advection_rate * (
                    self.airflow_grid[i, j] - self.airflow_grid[i - 1, j]
                )

                # Terme de la diffusion de l'air
                diffused_value = advected_value + diffusion_rate * (
                        self.airflow_grid[i - 1, j] + self.airflow_grid[i + 1, j] +
                        self.airflow_grid[i, j - 1] + self.airflow_grid[i, j + 1] - 
                        4 * self.airflow_grid[i, j]
                )
    
                new_airflow_grid[i, j] = diffused_value
        
        self.airflow_grid = new_airflow_grid

    def update_plot(self):
        # Mise à jour du graphique avec les données du moment
        self.figure.clear()
        ax = self.figure.add_subplot(111, projection='3d')
        x = np.arange(0, self.grid_size[1])
        y = np.arange(0, self.grid_size[0])
        X, Y = np.meshgrid(x, y)
        Z = self.airflow_grid
        
        # Création du graphique avec les donnéesen 3d
        ax.plot_surface(X, Y, Z, cmap='viridis')

        # Ajout des lignes de champs de l'écoulement d'air
        step_size = 2 # Ajuster en fonction des performances
        ax.quiver(X[::step_size, ::step_size], Y[::step_size, ::step_size], Z[::step_size, ::step_size],
                  self.airflow_grid[::step_size, ::step_size],
                  self.airflow_grid[::step_size, ::step_size],
                  self.airflow_grid[::step_size, ::step_size],
                  length=0.1, normalize=True, color='red')

        ax.set_xlabel('Axe_X')
        ax.set_ylabel('Axe_Y')
        ax.set_zlabel('Airflow')
        ax.set_title('Airflow Simulator')
        self.canvas.draw()

    def start_simulation(self):
        self.initialize_simulation()
        self.run_simulation()
        # Pour simplifier nous affichons la grille finale de l'écoulement d'air

def main():
    app = QApplication(sys.argv)
    window = AirflowSimulator(grid_size=(20, 20), time_steps=100)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()