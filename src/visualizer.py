import plotly.graph_objects as go

class TreeVisualizer:
    def __init__(self, tree):
        self.tree = tree

    def add_edges(self, fig):
        """
        Agregar aristas
        """
        # Graficar aristas
        for i in range(self.tree.edges.shape[0]):
            for j in range(self.tree.edges.shape[1]):
                if self.tree.edges[i, j] == 1:  # Si hay una conexión entre i y j
                    fig.add_trace(go.Scatter3d(
                        x=[self.tree.nodes_positions[i, 0], self.tree.nodes_positions[j, 0]],
                        y=[self.tree.nodes_positions[i, 1], self.tree.nodes_positions[j, 1]],
                        z=[self.tree.nodes_positions[i, 2], self.tree.nodes_positions[j, 2]],
                        mode='lines',
                        line=dict(color='gray', width=2),
                        showlegend=False
                    ))

    def plot_3d_tree(self, tree, img_name):
        """
        Grafica el árbol en 3D con Plotly
        """
        # Crear una figura 3D
        fig = go.Figure()

        # Graficar nodos
        fig.add_trace(go.Scatter3d(
            x=tree.nodes_positions[:, 0],
            y=tree.nodes_positions[:, 1],
            z=tree.nodes_positions[:, 2],
            mode='markers+text',
            marker=dict(size=10, color='#d2b4de'),
            text=[str(i) for i in range(tree.nodes_positions.shape[0])],
            textposition='top center',
            name='Nodes'
        ))

        self.add_edges(fig)

        # firefighter_positions = np.array(tree.get_firefighter_positions())
        # if firefighter_positions.size > 0:
        #     fig.add_trace(go.Scatter3d(
        #         x=firefighter_positions[:, 0],
        #         y=firefighter_positions[:, 1],
        #         z=firefighter_positions[:, 2],
        #         mode='markers',
        #         marker=dict(size=10, color='green'),
        #         name='Firefighters'
        #     ))

        fig.update_layout(title='3D Tree Structure',
                scene=dict(
                    xaxis=dict(title='X Axis', range=[-1, 1]),
                    yaxis=dict(title='Y Axis', range=[-1, 1]),
                    zaxis=dict(title='Z Axis', range=[-1, 1])
                ),
                width=700,
                height=700)

        fig.write_html(img_name + ".html")

    def plot_fire_state(self, burning_nodes, burned_nodes, step, protected_nodes, firefighter_position):
        """
        Genera y guarda una imagen 3D del estado actual de la propagación del incendio.
        """
        fig = go.Figure()

        # Nodos en llamas (burning)
        fig.add_trace(go.Scatter3d(
            x=[self.tree.nodes_positions[node, 0] for node in burning_nodes],
            y=[self.tree.nodes_positions[node, 1] for node in burning_nodes],
            z=[self.tree.nodes_positions[node, 2] for node in burning_nodes],
            mode='markers',
            marker=dict(size=5, color='black'),
            name='Burning Nodes'
        ))

        # Nodos quemados (burned)
        fig.add_trace(go.Scatter3d(
            x=[self.tree.nodes_positions[node, 0] for node in burned_nodes],
            y=[self.tree.nodes_positions[node, 1] for node in burned_nodes],
            z=[self.tree.nodes_positions[node, 2] for node in burned_nodes],
            mode='markers',
            marker=dict(size=5, color='black'),
            name='Burned Nodes'
        ))

        # Nodos protegidos (protected)
        if protected_nodes:
            fig.add_trace(go.Scatter3d(
                x=[self.tree.nodes_positions[node, 0] for node in protected_nodes],
                y=[self.tree.nodes_positions[node, 1] for node in protected_nodes],
                z=[self.tree.nodes_positions[node, 2] for node in protected_nodes],
                mode='markers',
                marker=dict(size=5, color='yellow'),
                name='Protected Nodes'
            ))

        # Nodos que no han sido quemados ni están en llamas (restantes)
        all_nodes = set(range(self.tree.nodes_positions.shape[0]))
        unaffected_nodes = all_nodes - burning_nodes - burned_nodes

        if protected_nodes:
            unaffected_nodes = unaffected_nodes - protected_nodes

        fig.add_trace(go.Scatter3d(
            x=[self.tree.nodes_positions[node, 0] for node in unaffected_nodes],
            y=[self.tree.nodes_positions[node, 1] for node in unaffected_nodes],
            z=[self.tree.nodes_positions[node, 2] for node in unaffected_nodes],
            mode='markers',
            marker=dict(size=5, color='blue'),
            name='Unaffected Nodes'
        ))

        # Agregar aristas entre nodos
        for i in range(self.tree.edges.shape[0]):
            for j in range(self.tree.edges.shape[1]):
                if self.tree.edges[i, j] == 1:
                    fig.add_trace(go.Scatter3d(
                    x=[self.tree.nodes_positions[i, 0], self.tree.nodes_positions[j, 0]],
                    y=[self.tree.nodes_positions[i, 1], self.tree.nodes_positions[j, 1]],
                    z=[self.tree.nodes_positions[i, 2], self.tree.nodes_positions[j, 2]],
                    mode='lines',
                    line=dict(color='gray', width=2),
                    showlegend=False
                    ))

        # Agregar posicion del bombero
        fig.add_trace(go.Scatter3d(
            x=[firefighter_position[0]],
            y=[firefighter_position[1]],
            z=[firefighter_position[2]],
            mode='markers',
            marker=dict(size=5, color='green'),
            name='Firefighter'
        ))

        # Configuracion
        fig.update_layout(title=f'Step {step}: Fire Propagation',
                        scene=dict(xaxis=dict(title='X Axis', range=[-1, 1]),
                                   yaxis=dict(title='Y Axis', range=[-1, 1]),
                                   zaxis=dict(title='Z Axis', range=[-1, 1])),
                        width=700, height=700)

        # Guardar la imagen
        fig.write_image(f"images/states/state_{step}.png")

    def plot_3d_final_state(self, burning_nodes, burned_nodes, protected_nodes, firefighter_position):
        """
        Genera y guarda una imagen 3D del estado final de la propagación del incendio.
        """
        fig = go.Figure()

        # Nodos en llamas (burning)
        fig.add_trace(go.Scatter3d(
            x=[self.tree.nodes_positions[node, 0] for node in burning_nodes],
            y=[self.tree.nodes_positions[node, 1] for node in burning_nodes],
            z=[self.tree.nodes_positions[node, 2] for node in burning_nodes],
            mode='markers',
            marker=dict(size=8, color='black'),
            name='Burning Nodes'
        ))

        # Nodos quemados (burned)
        fig.add_trace(go.Scatter3d(
            x=[self.tree.nodes_positions[node, 0] for node in burned_nodes],
            y=[self.tree.nodes_positions[node, 1] for node in burned_nodes],
            z=[self.tree.nodes_positions[node, 2] for node in burned_nodes],
            mode='markers',
            marker=dict(size=8, color='black'),
            name='Burned Nodes'
        ))

        # Nodos protegidos (protected)
        if protected_nodes:
            fig.add_trace(go.Scatter3d(
                x=[self.tree.nodes_positions[node, 0] for node in protected_nodes],
                y=[self.tree.nodes_positions[node, 1] for node in protected_nodes],
                z=[self.tree.nodes_positions[node, 2] for node in protected_nodes],
                mode='markers',
                marker=dict(size=8, color='yellow'),
                name='Protected Nodes'
            ))

        # Nodos que no han sido quemados ni están en llamas (restantes)
        all_nodes = set(range(self.tree.nodes_positions.shape[0]))
        unaffected_nodes = all_nodes - burning_nodes - burned_nodes

        if protected_nodes:
            unaffected_nodes = unaffected_nodes - protected_nodes

        fig.add_trace(go.Scatter3d(
            x=[self.tree.nodes_positions[node, 0] for node in unaffected_nodes],
            y=[self.tree.nodes_positions[node, 1] for node in unaffected_nodes],
            z=[self.tree.nodes_positions[node, 2] for node in unaffected_nodes],
            mode='markers',
            marker=dict(size=8, color='blue'),
            name='Unaffected Nodes'
        ))

        # Agregar aristas entre nodos
        for i in range(self.tree.edges.shape[0]):
            for j in range(self.tree.edges.shape[1]):
                if self.tree.edges[i, j] == 1:
                    fig.add_trace(go.Scatter3d(
                    x=[self.tree.nodes_positions[i, 0], self.tree.nodes_positions[j, 0]],
                    y=[self.tree.nodes_positions[i, 1], self.tree.nodes_positions[j, 1]],
                    z=[self.tree.nodes_positions[i, 2], self.tree.nodes_positions[j, 2]],
                    mode='lines',
                    line=dict(color='gray', width=2),
                    showlegend=False
                    ))

        # Agregar posicion del bombero
        fig.add_trace(go.Scatter3d(
            x=[firefighter_position[0]],
            y=[firefighter_position[1]],
            z=[firefighter_position[2]],
            mode='markers',
            marker=dict(size=10, color='green'),
            name='Firefighter'
        ))

        # Configuracion
        fig.update_layout(title='Final State: Fire Propagation',
                scene=dict(xaxis=dict(title='X Axis', range=[-1, 1]),
                       yaxis=dict(title='Y Axis', range=[-1, 1]),
                       zaxis=dict(title='Z Axis', range=[-1, 1])),
                width=900, height=900)
        
        # Guardar html
        fig.write_html("images/final_state.html")

