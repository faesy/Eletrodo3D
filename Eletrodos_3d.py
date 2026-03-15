import pyvista as pv
import numpy as np
import vtk
import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QFileDialog, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QCheckBox, QComboBox, QScrollArea, QSizePolicy,
    QDoubleSpinBox, QLabel
)
from PyQt5.QtCore import QTimer

app = QApplication([])
# -----------------------------
#  Idioma
# -----------------------------
CURRENT_LANG = "pt-BR"

TRANSLATIONS = {
    "pt-BR": {
        # Geral
        "window_control_title": "Controle dos Eletrodos",
        "window_camera_title": "Controle de Câmera",
        "language_label": "Idioma:",
        "lang_pt": "Português (BR)",
        "lang_en": "English",
        "step_label": "Passo:",

        # Botões - controle de eletrodos
        "add_electrode": "Adicionar Eletrodo",
        "remove_last": "Remover Último Eletrodo",
        "save": "Salvar",
        "import": "Importar",
        "close": "Fechar",

        # Toggles
        "front_snap_on": "Fixar na frente (Y mínimo): ON",
        "front_snap_off": "Fixar na frente (Y mínimo): OFF",
        "front_snap_tooltip": "Quando ON, o clique fixa no Y mínimo (frente). Quando OFF, o clique usa a superfície (laterais OK).",
        "window_only_on": "Controle somente pela janela: ON",
        "window_only_off": "Controle somente pela janela: OFF",
        "window_only_tooltip": "Quando ON, cliques no torso são ignorados. Os botões X/Y/Z continuam funcionando.",

        # Botões de movimento livre
        "axis_x_neg": "X-",
        "axis_x_pos": "X+",
        "axis_y_neg": "Y-",
        "axis_y_pos": "Y+",
        "axis_z_neg": "Z-",
        "axis_z_pos": "Z+",

        # Janela da câmera
        "cam_x_pos": "Camera X+",
        "cam_x_neg": "Camera X-",
        "cam_y_pos": "Camera Y+",
        "cam_y_neg": "Camera Y-",
        "cam_z_pos": "Camera Z+",
        "cam_z_neg": "Camera Z-",
        "cam_left": "Ângulo Esq.",
        "cam_right": "Ângulo Dir.",
        "cam_up": "Ângulo Cima",
        "cam_down": "Ângulo Baixo",
        "cam_reset": "Reset Camera",

        # Diálogos
        "select_folder": "Selecionar Pasta com Arquivos VTP",
        "save_electrodes": "Salvar coordenadas dos eletrodos",
        "import_electrodes": "Importar coordenadas dos eletrodos",

        # Erros / mensagens
        "error_no_folder": "Nenhuma pasta selecionada.",
        "error_no_vtp": "Nenhum arquivo .vtp encontrado na pasta selecionada.",
        "error_no_torso": "Nenhuma malha com 'torso' no nome foi encontrada para posicionar os eletrodos.",
        "warning_no_actor": "[AVISO] Sem actor associado para '{fname}' (possivelmente 'Linha' ou não renderizado).",
        "warning_no_plane": "[AVISO] '{name}' tem menos de 3 pontos - não é possível ajustar um plano.",
        "warning_no_intersection": "[AVISO] Sem interseção detectada para '{name}' (slice vazio).",
        "no_electrode_remove": "Nenhum eletrodo para remover.",
        "electrode_added": "Eletrodo ({label}) adicionado em: X={x:.2f}, Y={y:.2f}, Z={z:.2f}",
        "electrode_removed": "Último eletrodo removido: {label}.",
        "electrode_remaining": "Número de eletrodos restantes: {n}",
        "camera_mode_on": "Modo de controle de câmera ativado.",
        "camera_mode_off": "Modo de controle de câmera desativado.",
        "file_saved": "Arquivo '{path}' salvo com sucesso!",
        "file_imported": "Arquivo '{path}' importado com sucesso!",
        "line_import_error": "Erro ao ler linha:\n  {line}\n→ {err}",
        "candidates_found": "Encontrados {n} pontos candidatos com tol={tol}",
        "key_pressed": "Tecla pressionada: {key}",

        # Câmera print
        "camera_header": "----- Câmera -----",
        "camera_position": "  Position = {pos}",
        "camera_focal": "  Focal point = {focal}",
        "camera_angles": "  Azimuth = {az:.2f}°, Elevation = {el:.2f}°",
        "camera_footer": "------------------",
    },

    "en": {
        # Geral
        "window_control_title": "Electrode Control",
        "window_camera_title": "Camera Control",
        "language_label": "Language:",
        "lang_pt": "Português (BR)",
        "lang_en": "English",
        "step_label": "Step:",

        # Botões - controle de eletrodos
        "add_electrode": "Add Electrode",
        "remove_last": "Remove Last Electrode",
        "save": "Save",
        "import": "Import",
        "close": "Close",

        # Toggles
        "front_snap_on": "Fix to front (minimum Y): ON",
        "front_snap_off": "Fix to front (minimum Y): OFF",
        "front_snap_tooltip": "When ON, click locks to the minimum Y (front). When OFF, click uses the surface (side positions allowed).",
        "window_only_on": "Control only from window: ON",
        "window_only_off": "Control only from window: OFF",
        "window_only_tooltip": "When ON, clicks on the torso are ignored. The X/Y/Z buttons still work.",

        # Botões de movimento livre
        "axis_x_neg": "X-",
        "axis_x_pos": "X+",
        "axis_y_neg": "Y-",
        "axis_y_pos": "Y+",
        "axis_z_neg": "Z-",
        "axis_z_pos": "Z+",

        # Janela da câmera
        "cam_x_pos": "Camera X+",
        "cam_x_neg": "Camera X-",
        "cam_y_pos": "Camera Y+",
        "cam_y_neg": "Camera Y-",
        "cam_z_pos": "Camera Z+",
        "cam_z_neg": "Camera Z-",
        "cam_left": "Angle Left",
        "cam_right": "Angle Right",
        "cam_up": "Angle Up",
        "cam_down": "Angle Down",
        "cam_reset": "Reset Camera",

        # Diálogos
        "select_folder": "Select Folder with VTP Files",
        "save_electrodes": "Save electrode coordinates",
        "import_electrodes": "Import electrode coordinates",

        # Erros / mensagens
        "error_no_folder": "No folder selected.",
        "error_no_vtp": "No .vtp files found in the selected folder.",
        "error_no_torso": "No mesh containing 'torso' in its name was found for electrode placement.",
        "warning_no_actor": "[WARNING] No actor associated with '{fname}' (possibly a 'Linha' file or not rendered).",
        "warning_no_plane": "[WARNING] '{name}' has fewer than 3 points - it is not possible to fit a plane.",
        "warning_no_intersection": "[WARNING] No intersection detected for '{name}' (empty slice).",
        "no_electrode_remove": "No electrode to remove.",
        "electrode_added": "Electrode ({label}) added at: X={x:.2f}, Y={y:.2f}, Z={z:.2f}",
        "electrode_removed": "Last electrode removed: {label}.",
        "electrode_remaining": "Number of remaining electrodes: {n}",
        "camera_mode_on": "Camera control mode enabled.",
        "camera_mode_off": "Camera control mode disabled.",
        "file_saved": "File '{path}' saved successfully!",
        "file_imported": "File '{path}' imported successfully!",
        "line_import_error": "Error reading line:\n  {line}\n→ {err}",
        "candidates_found": "Found {n} candidate points with tol={tol}",
        "key_pressed": "Key pressed: {key}",

        # Câmera print
        "camera_header": "----- Camera -----",
        "camera_position": "  Position = {pos}",
        "camera_focal": "  Focal point = {focal}",
        "camera_angles": "  Azimuth = {az:.2f}°, Elevation = {el:.2f}°",
        "camera_footer": "------------------",
    }
}

def tr(key, **kwargs):
    text = TRANSLATIONS[CURRENT_LANG].get(key, key)
    return text.format(**kwargs) if kwargs else text
# -----------------------------
#  SELEÇÃO DE PASTA E LEITURA
# -----------------------------
folder_path = QFileDialog.getExistingDirectory(None, tr("select_folder"))
if not folder_path:
    raise Exception(tr("error_no_folder"))

vtp_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.vtp')]
# Ordem estável para a paleta não "pular"
vtp_files = sorted(vtp_files, key=lambda p: os.path.basename(p).lower())

# Estilo fixo para torso (cinza claro translúcido) e demais
TORSO_COLOR   = (0.90, 0.90, 0.90)
TORSO_OPACITY = 0.25       # ajuste se quiser mais/menos translúcido
OUT_OPACITY   = 0.90       # opacidade das outras malhas
PLANE_OPACITY = 0.25       # opacidade dos planos

if not vtp_files:
    raise Exception("error_no_vtp")

# Paleta daltônico-safe (Okabe–Ito + extensões suaves), sem cinzas
color_palette = [
    [0.90, 0.60, 0.00],  # laranja
    [0.95, 0.90, 0.25],  # amarelo
    [0.35, 0.70, 0.90],  # azul-claro
    [0.00, 0.62, 0.45],  # verde
    [0.80, 0.47, 0.74],  # roxo
    [0.80, 0.40, 0.00],  # laranja-escuro
    [0.36, 0.35, 0.63],  # azul-arroxeado
    [0.94, 0.55, 0.55],  # vermelho-claro
    [0.40, 0.76, 0.65],  # verde-acinzentado
    [0.55, 0.63, 0.80],  # azul acinzentado
    [0.65, 0.85, 0.33],  # verde-lima
    [0.90, 0.67, 0.50],  # pêssego
    [0.55, 0.34, 0.29],  # marrom
    [0.50, 0.50, 0.00],  # oliva
]


# Separar malhas para renderização e para projeção dos eletrodos
render_meshes = []          # tudo que não for "Linha" (continua sendo exibido e com checkbox)
render_filenames = []
torso_proj_meshes = []      # APENAS arquivos com "torso" no nome (para snap dos eletrodos)
torso_proj_filenames = []
linha_raw_points = []       # lista de dicts com info para gerar plano depois
linha_filenames = []


for file_path in vtp_files:
    name = os.path.basename(file_path)
    mesh = pv.read(file_path)

    # "Linha" -> só para gerar planos auxiliares
    if 'linha' in name.lower():
        if mesh.n_points >= 3:
            pts = np.asarray(mesh.points)
            linha_raw_points.append({'name': name, 'points': pts})
            linha_filenames.append(name)
        else:
            print(tr("warning_no_plane", name=name))
        continue

    # Render: todo VTP que não é "Linha" continua visível/controlável
    if 'Normals' not in mesh.point_data:
        mesh.compute_normals(inplace=True)
    render_meshes.append(mesh)
    render_filenames.append(name)

    # Projeção: apenas nomes contendo "torso"
    if 'torso' in name.lower():
        torso_proj_meshes.append(mesh)
        torso_proj_filenames.append(name)

if not torso_proj_meshes:
    raise Exception(tr("error_no_torso"))


# -----------------------------
#  PLOTTER E MALHAS
# -----------------------------
plotter = pv.Plotter()

# Posição inicial da câmera
INITIAL_CAM_POS = (33.92955911088626, -868.6406385699812, 72.59394144121086)
INITIAL_CAM_FOCAL = (15.194366455078125, -14.439411163330078, -25.041778564453125)

plotter.camera.position = INITIAL_CAM_POS
plotter.camera.focal_point = INITIAL_CAM_FOCAL
plotter.camera.azimuth = 0.0
plotter.camera.elevation = 0.0

# Renderizar malhas (todas que não são 'Linha')
file_actor_map = {}
torso_actors = []
palette_idx = 0

for i, mesh in enumerate(render_meshes):
    fname_lower = render_filenames[i].lower()

    # Garante normais
    if 'Normals' not in mesh.point_data:
        mesh.compute_normals(inplace=True)

    if 'torso' in fname_lower:
        # Torso sempre cinza claro translúcido
        actor = plotter.add_mesh(
            mesh,
            color=TORSO_COLOR,
            opacity=TORSO_OPACITY,
            label=f"Mesh {i+1}: {render_filenames[i]}",
            smooth_shading=True
        )
        torso_actors.append(actor)
    else:
        # Demais estruturas com paleta alto-contraste
        color = color_palette[palette_idx % len(color_palette)]
        palette_idx += 1
        actor = plotter.add_mesh(
            mesh,
            color=color,
            opacity=OUT_OPACITY,
            label=f"Mesh {i+1}: {render_filenames[i]}",
            smooth_shading=True
        )

    file_actor_map[render_filenames[i]] = actor


plotter.add_legend()

# MultiBlock para PROJEÇÃO dos eletrodos (apenas 'torso*')
mb_proj = pv.MultiBlock(torso_proj_meshes)
mesh_torso_proj = mb_proj.combine()
plotter.add_mesh(mesh_torso_proj, opacity=0)  # invisível; usado só para o snap


# Criar planos auxiliares a partir dos VTPs "Linha"
def best_fit_plane(points: np.ndarray):
    """
    Retorna (centro, normal) do melhor plano por PCA.
    """
    c = points.mean(axis=0)
    A = points - c
    # Autovetores da covariância
    _, _, vt = np.linalg.svd(A, full_matrices=False)
    normal = vt[-1, :]  # menor autovalor → normal do plano
    # normal normalizada
    normal = normal / (np.linalg.norm(normal) + 1e-12)
    return c, normal

bounds = mesh_torso_proj.bounds  # (xmin,xmax,ymin,ymax,zmin,zmax)
size_max = max(bounds[1]-bounds[0], bounds[3]-bounds[2], bounds[5]-bounds[4]) * 1.2
if size_max <= 0:
    size_max = 100.0  # fallback

linha_plane_meshes = []
linha_plane_actors = []
linha_planes_info = []
for i, item in enumerate(linha_raw_points):
    center, normal = best_fit_plane(item['points'])
    plane = pv.Plane(center=center, direction=normal, i_size=size_max, j_size=size_max, i_resolution=1, j_resolution=1)

    # ✅ guarde os dados para o slice depois
    linha_planes_info.append({'name': item['name'], 'center': center, 'normal': normal})

    linha_plane_meshes.append(plane)
    color = color_palette[(len(torso_proj_meshes) + i) % len(color_palette)]
    actor = plotter.add_mesh(plane, color=color, opacity=0.25, label=f"Plano: {item['name']}")
    linha_plane_actors.append(actor)
    file_actor_map[item['name']] = actor
# ---- INTERSEÇÕES TORSO x PLANOS (realce em vermelho) ----
intersection_actors = []
for info in linha_planes_info:
    # Faz o slice do torso combinado por cada plano (definido por origem/normal)
    slc = mesh_torso_proj.slice(origin=info['center'], normal=info['normal'])

    if slc.n_points > 1:
        # Tubo grosso pra destacar a linha (ajuste o raio conforme escala do teu modelo)
        try:
            tube = slc.tube(radius=max(size_max * 0.005, 2.0), n_sides=24)
            actor = plotter.add_mesh(
                tube, color=(1.0, 0.0, 0.0), opacity=1.0,
                label=f"Interseção: {info['name']}", lighting=False
            )
        except Exception:
            # fallback se tube não estiver disponível por algum motivo
            actor = plotter.add_mesh(
                slc, color=(1.0, 0.0, 0.0), opacity=1.0,
                line_width=6, render_lines_as_tubes=True,
                label=f"Interseção: {info['name']}", lighting=False
            )
        intersection_actors.append(actor)
    else:
        print(f"[AVISO] Sem interseção detectada para '{info['name']}' (slice vazio).")



plotter.add_legend(size=(0, 0))  # reposicionar legenda se necessário


# -----------------------------s
#  ESFERA DE PREVIEW
# -----------------------------
sphere_radius = 6
preview_sphere = pv.Sphere(radius=sphere_radius)
preview_actor = plotter.add_mesh(preview_sphere, color='blue', opacity=1)
initial_position = np.mean(mesh_torso_proj.points, axis=0)
preview_actor.SetPosition(initial_position)

line_actor = None
is_preview_active = True
current_preview_position = np.array(initial_position)

# =========================================
#  ESTRUTURAS GLOBAIS P/ ELETRODOS
# =========================================
electrodes = []
electrode_actors = {}
is_space_pressed = False

# Novo: modo de snap
front_snap_enabled = True  # True = fixa no Y mínimo (frente); False = gruda na superfície (laterais possíveis)

# Modo: controles da janela apenas (ignora clique no plotter quando ON)
window_only_mode = False

def snap_point_to_torso(target_pos):
    """
    Retorna um ponto na superfície do torso conforme o modo:
      - front_snap_enabled=True: usa o menor Y do vizinho (frente)
      - front_snap_enabled=False: usa o ponto mais próximo na superfície (permite laterais)
    """
    target_pos = np.asarray(target_pos, dtype=float)

    if front_snap_enabled:
        # comportamento atual (frente): menor Y para o XZ selecionado
        candidate_point = find_lowest_y_point(target_pos)
        snapped = find_lowest_y_for_xz(candidate_point, tol=1.0)
        return snapped
    else:
        # lateral/superfície: ponto mais próximo na superfície
        pid = mesh_torso_proj.find_closest_point(target_pos)
        return mesh_torso_proj.points[pid]

# --------------------------------------
# HELPER: cria ou substitui 1 eletrodo
# --------------------------------------
def create_or_replace_electrode(label, position):
    """
    Remove marca antiga (caso exista) e cria novo 'label' em 'position'.
    Adiciona/atualiza a lista electrodes e o dicionário electrode_actors.
    Todos os eletrodos são tratados da mesma forma.
    """
    global electrodes, electrode_actors

    # Se o label já existe, remove do plotter e da lista 'electrodes'
    if label in electrode_actors:
        old_sphere, old_text = electrode_actors[label]
        plotter.remove_actor(old_sphere)
        plotter.remove_actor(old_text)
        electrodes = [(lbl, pos) for (lbl, pos) in electrodes if lbl != label]

    # Cria nova esfera
    sphere_actor = plotter.add_mesh(
        pv.Sphere(radius=3, center=position),
        color='green', opacity=1.0
    )

    # Cria o texto (rótulo)
    text_actor = plotter.add_point_labels(
        [position],
        [label],
        font_size=8,
        point_size=5,
        always_visible=True
    )

    electrode_actors[label] = (sphere_actor, text_actor)
    electrodes.append((label, position))

    print("\n" + tr(
    "electrode_added",
    label=label,
    x=position[0],
    y=position[1],
    z=position[2]
    ))

# -----------------------------
#  FUNÇÕES PRINCIPAIS
# -----------------------------
def add_electrode():
    """
    Adiciona manualmente o eletrodo selecionado na posição atual do preview.
    Não há mais posicionamento automático de eletrodos de membro.
    """
    global preview_actor
    label = control_window.combo_label.currentText()
    pos = preview_actor.GetPosition()

    create_or_replace_electrode(label, pos)
    plotter.render()

def remove_last_electrode():
    """
    Remove o último eletrodo adicionado,
    apaga do plotter e do dicionário de atores.
    """
    global electrodes, electrode_actors
    if not electrodes:
        print(tr("no_electrode_remove"))
        return

    # "Pop" retira o último item (label, posição)
    last_label, last_pos = electrodes.pop()

    if last_label in electrode_actors:
        sphere_actor, text_actor = electrode_actors[last_label]
        plotter.remove_actor(sphere_actor)
        plotter.remove_actor(text_actor)
        del electrode_actors[last_label]

    print(tr("electrode_removed", label=last_label))
    print(tr("electrode_remaining", n=len(electrodes)))

def find_lowest_y_point(mouse_position, tol=None):
    closest_point_id = mesh_torso_proj.find_closest_point(mouse_position)
    closest_point = mesh_torso_proj.points[closest_point_id]
    x, z = closest_point[0], closest_point[2]
    if tol is None:
        bounds = mesh_torso_proj.bounds
        tol = (bounds[1] - bounds[0]) * 0.01
    mask = np.linalg.norm(mesh_torso_proj.points[:, [0,2]] - np.array([x, z]), axis=1) < tol
    candidates = mesh_torso_proj.points[mask]
    print(f"Encontrados {len(candidates)} pontos candidatos com tol={tol}")

    if candidates.size > 0:
        lowest_y_point = candidates[np.argmin(candidates[:, 1])]
        return lowest_y_point
    else:
        return closest_point

def find_lowest_y_for_xz(candidate_point, tol=1.0):
    x_candidate, z_candidate = candidate_point[0], candidate_point[2]
    mask = (np.abs(mesh_torso_proj.points[:, 0] - x_candidate) < tol) & \
           (np.abs(mesh_torso_proj.points[:, 2] - z_candidate) < tol)
    candidates = mesh_torso_proj.points[mask]
    if candidates.size > 0:
        lowest_y_point = candidates[np.argmin(candidates[:, 1])]
        return lowest_y_point
    else:
        return candidate_point

def on_left_click(iren, event):
    global is_preview_active, current_preview_position, window_only_mode
    # Quando ativado, clique não faz nada
    if window_only_mode:
        return

    if is_preview_active and not is_space_pressed:
        mouse_pos = plotter.pick_mouse_position()
        if mouse_pos is not None:
            snapped = snap_point_to_torso(mouse_pos)
            preview_actor.SetPosition(snapped)
            current_preview_position = snapped
            plotter.render()


def move_preview(iren, event):
    global current_preview_position, preview_actor, is_space_pressed
    if is_space_pressed:
        return

    delta = 1.0
    key = iren.GetKeySym()
    new_position = np.copy(current_preview_position)

    if key == 'Up':
        new_position[2] += delta
    elif key == 'Down':
        new_position[2] -= delta
    elif key == 'Left':
        new_position[0] -= delta
    elif key == 'Right':
        new_position[0] += delta
    else:
        return

    # Snap sempre à superfície/“frente” conforme o modo
    snapped = snap_point_to_torso(new_position)
    preview_actor.SetPosition(snapped)
    current_preview_position = snapped
    plotter.render()



def capture_key_events(iren, event):
    global is_space_pressed, key
    key = iren.GetKeySym()
    print(f"Tecla pressionada: {key}")

    if key == 'Return':
        add_electrode()
    elif key == 'Backspace':
        remove_last_electrode()
    elif key == 'space':
        is_space_pressed = not is_space_pressed
        print("Modo de controle de câmera " + ("ativado." if is_space_pressed else "desativado."))
    elif key == 's':
        save_files()

def save_files():
    global electrodes
    txt_file_path, _ = QFileDialog.getSaveFileName(
        None, tr("save_electrodes"),
        "", "TXT files (*.txt);;All files (*)"
    )
    if txt_file_path:
        with open(txt_file_path, 'w') as f:
            for idx, (label, position) in enumerate(electrodes, start=1):
                f.write(f"Eletrodo #{idx} ({label}): "
                        f"X={position[0]:.2f}, Y={position[1]:.2f}, Z={position[2]:.2f}\n")
        print(f"Arquivo '{txt_file_path}' salvo com sucesso!")
        
# -------------------------------------------------
#  IMPORTAR COORDENADAS SALVAS
# -------------------------------------------------
def import_files():
    """
    Abre um .txt salvo pelo programa, apaga quaisquer
    eletrodos já existentes e recria todos os pontos
    (esferas + rótulos) a partir do arquivo.
    """
    global electrodes, electrode_actors

    txt_file_path, _ = QFileDialog.getOpenFileName(
        None,
        tr("import_electrodes"),
        "",
        "TXT files (*.txt);;All files (*)"
    )
    if not txt_file_path:
        return  # usuário cancelou

    # 1) Remove tudo que já existe
    for sphere_act, text_act in electrode_actors.values():
        plotter.remove_actor(sphere_act)
        plotter.remove_actor(text_act)
    electrodes.clear()
    electrode_actors.clear()

    # 2) Lê cada linha do arquivo e recria o ponto
    with open(txt_file_path, "r") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                # Ex.: "Eletrodo #3 (V2): X=10.00, Y=20.00, Z=30.00"
                label = line.split("(")[1].split(")")[0]
                coord_str = line.split(":")[1]
                x = float(coord_str.split("X=")[1].split(",")[0])
                y = float(coord_str.split("Y=")[1].split(",")[0])
                z = float(coord_str.split("Z=")[1])
                create_or_replace_electrode(label, (x, y, z))
            except Exception as e:
                print(f"Erro ao ler linha:\n  {line.strip()}\n→ {e}")

    plotter.render()
    print(f"Arquivo '{txt_file_path}' importado com sucesso!")


def move_preview_free(dx=0.0, dy=0.0, dz=0.0, step=1.0):
    """
    Move a esfera de preview livremente (sem snap).
    dx, dy, dz são multiplicados por 'step'.
    """
    global current_preview_position, preview_actor
    new_position = np.array(preview_actor.GetPosition(), dtype=float)
    new_position += np.array([dx, dy, dz], dtype=float) * float(step)
    preview_actor.SetPosition(new_position)
    current_preview_position = new_position
    plotter.render()


# ---------------------------------------------------
#   JANELA 1: CONTROLE DE ELETRODOS
# ---------------------------------------------------

class ControlWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(1100, 100, 300, 550)

        main_layout = QVBoxLayout(self)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        scroll_widget = QWidget()
        scroll_area.setWidget(scroll_widget)

        layout = QVBoxLayout(scroll_widget)

        # -------------------------
        # Idioma
        # -------------------------
        self.language_row = QHBoxLayout()
        self.language_label = QLabel()
        self.language_combo = QComboBox()
        self.language_combo.addItem(TRANSLATIONS["pt-BR"]["lang_pt"], "pt-BR")
        self.language_combo.addItem(TRANSLATIONS["en"]["lang_en"], "en")
        self.language_combo.setCurrentIndex(0 if CURRENT_LANG == "pt-BR" else 1)
        self.language_combo.currentIndexChanged.connect(self.change_language)

        self.language_row.addWidget(self.language_label)
        self.language_row.addWidget(self.language_combo)
        layout.addLayout(self.language_row)

        # ComboBox com rótulos
        self.combo_label = QComboBox()
        electrode_labels = ["V1","V2","V3","V4","V5","V6","LA","RA","LL","RL"]
        self.combo_label.addItems(electrode_labels)
        layout.addWidget(self.combo_label)

        # -------------------------
        # Botões de movimentação
        # -------------------------
        move_layout = QVBoxLayout()

        self.step_row = QHBoxLayout()
        self.step_label = QLabel()
        self.step_spin = QDoubleSpinBox()
        self.step_spin.setDecimals(2)
        self.step_spin.setRange(0.01, 1000.0)
        self.step_spin.setSingleStep(0.25)
        self.step_spin.setValue(1.0)
        self.step_row.addWidget(self.step_label)
        self.step_row.addWidget(self.step_spin)
        move_layout.addLayout(self.step_row)

        def make_axis_controls(neg_key, pos_key, neg_cb, pos_cb):
            row = QHBoxLayout()
            btn_neg = QPushButton()
            btn_pos = QPushButton()
            btn_neg._translation_key = neg_key
            btn_pos._translation_key = pos_key

            timer_neg = QTimer()
            timer_pos = QTimer()

            def start_neg():
                neg_cb()
                timer_neg.start(80)

            def start_pos():
                pos_cb()
                timer_pos.start(80)

            timer_neg.timeout.connect(neg_cb)
            timer_pos.timeout.connect(pos_cb)

            btn_neg.pressed.connect(start_neg)
            btn_neg.released.connect(timer_neg.stop)
            btn_pos.pressed.connect(start_pos)
            btn_pos.released.connect(timer_pos.stop)

            row.addWidget(btn_neg)
            row.addWidget(btn_pos)
            return row, btn_neg, btn_pos

        def step_value():
            return float(self.step_spin.value())

        self.row_x, self.btn_x_neg, self.btn_x_pos = make_axis_controls(
            "axis_x_neg", "axis_x_pos",
            lambda: move_preview_free(dx=-1, dy=0, dz=0, step=step_value()),
            lambda: move_preview_free(dx=+1, dy=0, dz=0, step=step_value()),
        )

        self.row_y, self.btn_y_neg, self.btn_y_pos = make_axis_controls(
            "axis_y_neg", "axis_y_pos",
            lambda: move_preview_free(dx=0, dy=-1, dz=0, step=step_value()),
            lambda: move_preview_free(dx=0, dy=+1, dz=0, step=step_value()),
        )

        self.row_z, self.btn_z_neg, self.btn_z_pos = make_axis_controls(
            "axis_z_neg", "axis_z_pos",
            lambda: move_preview_free(dx=0, dy=0, dz=-1, step=step_value()),
            lambda: move_preview_free(dx=0, dy=0, dz=+1, step=step_value()),
        )

        move_layout.addLayout(self.row_x)
        move_layout.addLayout(self.row_y)
        move_layout.addLayout(self.row_z)
        layout.addLayout(move_layout)

        # -------------------------
        # Botões principais
        # -------------------------
        self.button_add = QPushButton()
        self.button_remove = QPushButton()
        self.button_save = QPushButton()
        self.button_close = QPushButton()
        self.button_import = QPushButton()

        self.button_add.clicked.connect(add_electrode)
        self.button_remove.clicked.connect(remove_last_electrode)
        self.button_save.clicked.connect(save_files)
        self.button_close.clicked.connect(lambda: sys.exit(0))
        self.button_import.clicked.connect(import_files)

        layout.addWidget(self.button_add)
        layout.addWidget(self.button_remove)
        layout.addWidget(self.button_save)
        layout.addWidget(self.button_import)
        layout.addWidget(self.button_close)

        # -------------------------
        # Toggles
        # -------------------------
        self.btn_toggle_front = QPushButton()
        self.btn_window_only = QPushButton()

        def refresh_toggle_texts():
            self.btn_toggle_front.setText(
                tr("front_snap_on") if front_snap_enabled else tr("front_snap_off")
            )
            self.btn_toggle_front.setToolTip(tr("front_snap_tooltip"))

            self.btn_window_only.setText(
                tr("window_only_on") if window_only_mode else tr("window_only_off")
            )
            self.btn_window_only.setToolTip(tr("window_only_tooltip"))

        self.refresh_toggle_texts = refresh_toggle_texts

        def on_toggle_front():
            global front_snap_enabled, current_preview_position
            front_snap_enabled = not front_snap_enabled
            self.refresh_ui_texts()
            snapped = snap_point_to_torso(preview_actor.GetPosition())
            preview_actor.SetPosition(snapped)
            current_preview_position = snapped
            plotter.render()

        def on_toggle_window_only():
            global window_only_mode
            window_only_mode = not window_only_mode
            self.refresh_ui_texts()

        self.btn_toggle_front.clicked.connect(on_toggle_front)
        self.btn_window_only.clicked.connect(on_toggle_window_only)

        layout.addWidget(self.btn_toggle_front)
        layout.addWidget(self.btn_window_only)

        # -------------------------
        # Checkboxes dos arquivos
        # -------------------------
        self.checkboxes = []
        for i, filename in enumerate(vtp_files):
            checkbox = QCheckBox(f"{os.path.basename(filename)}")
            checkbox.setChecked(True)
            checkbox.stateChanged.connect(lambda state, idx=i: self.toggle_mesh_visibility(idx, state))
            self.checkboxes.append(checkbox)
            layout.addWidget(checkbox)

        main_layout.addWidget(scroll_area)
        self.setFixedSize(300, 550)

        self.refresh_ui_texts()

    def refresh_ui_texts(self):
        self.setWindowTitle(tr("window_control_title"))
        self.language_label.setText(tr("language_label"))
        self.step_label.setText(tr("step_label"))

        self.button_add.setText(tr("add_electrode"))
        self.button_remove.setText(tr("remove_last"))
        self.button_save.setText(tr("save"))
        self.button_import.setText(tr("import"))
        self.button_close.setText(tr("close"))

        self.btn_x_neg.setText(tr("axis_x_neg"))
        self.btn_x_pos.setText(tr("axis_x_pos"))
        self.btn_y_neg.setText(tr("axis_y_neg"))
        self.btn_y_pos.setText(tr("axis_y_pos"))
        self.btn_z_neg.setText(tr("axis_z_neg"))
        self.btn_z_pos.setText(tr("axis_z_pos"))

        self.refresh_toggle_texts()

        if 'camera_window' in globals() and camera_window is not None:
            camera_window.refresh_ui_texts()

    def change_language(self):
        global CURRENT_LANG
        CURRENT_LANG = self.language_combo.currentData()
        self.refresh_ui_texts()

    def toggle_mesh_visibility(self, index, state):
        fname = os.path.basename(vtp_files[index])
        actor = file_actor_map.get(fname)
        if actor is None:
            print(tr("warning_no_actor", fname=fname))
            return

        visible = (state == 2)

        try:
            actor.SetVisibility(visible)
            actor.SetPickable(visible)
        except Exception:
            actor.GetProperty().SetOpacity(0.7 if visible else 0.0)

        plotter.render()



# ---------------------------------------------------
#  JANELA 2: CONTROLE DE CÂMERA (com reset)
# ---------------------------------------------------
class CameraControlWindow(QWidget):
    def __init__(self, plotter):
        super().__init__()
        self.plotter = plotter
        self.setGeometry(1450, 100, 300, 450)

        main_layout = QVBoxLayout()

        def move_camera(dx=0, dy=0, dz=0):
            cam_pos = list(self.plotter.camera.position)
            cam_pos[0] += dx
            cam_pos[1] += dy
            cam_pos[2] += dz
            self.plotter.camera.position = tuple(cam_pos)
            self.plotter.render()
            self.print_camera_state()

        def rotate_camera(direction):
            if direction == 'left':
                self.plotter.camera.azimuth += 5
            elif direction == 'right':
                self.plotter.camera.azimuth -= 5
            elif direction == 'up':
                self.plotter.camera.elevation += 5
            elif direction == 'down':
                self.plotter.camera.elevation -= 5

            self.plotter.render()
            self.print_camera_state()

        def reset_camera():
            self.plotter.camera.position = INITIAL_CAM_POS
            self.plotter.camera.focal_point = INITIAL_CAM_FOCAL
            self.plotter.camera.azimuth = 0.0
            self.plotter.camera.elevation = 0.0
            self.plotter.render()
            self.print_camera_state()

        self.btn_cam_x_pos = QPushButton()
        timer_cam_x_pos = QTimer()
        timer_cam_x_pos.timeout.connect(lambda: move_camera(dx=10))
        def on_press_cam_x_pos():
            move_camera(dx=10)
            timer_cam_x_pos.start(100)
        self.btn_cam_x_pos.pressed.connect(on_press_cam_x_pos)
        self.btn_cam_x_pos.released.connect(timer_cam_x_pos.stop)

        self.btn_cam_x_neg = QPushButton()
        timer_cam_x_neg = QTimer()
        timer_cam_x_neg.timeout.connect(lambda: move_camera(dx=-10))
        def on_press_cam_x_neg():
            move_camera(dx=-10)
            timer_cam_x_neg.start(100)
        self.btn_cam_x_neg.pressed.connect(on_press_cam_x_neg)
        self.btn_cam_x_neg.released.connect(timer_cam_x_neg.stop)

        self.btn_cam_y_pos = QPushButton()
        timer_cam_y_pos = QTimer()
        timer_cam_y_pos.timeout.connect(lambda: move_camera(dy=10))
        def on_press_cam_y_pos():
            move_camera(dy=10)
            timer_cam_y_pos.start(100)
        self.btn_cam_y_pos.pressed.connect(on_press_cam_y_pos)
        self.btn_cam_y_pos.released.connect(timer_cam_y_pos.stop)

        self.btn_cam_y_neg = QPushButton()
        timer_cam_y_neg = QTimer()
        timer_cam_y_neg.timeout.connect(lambda: move_camera(dy=-10))
        def on_press_cam_y_neg():
            move_camera(dy=-10)
            timer_cam_y_neg.start(100)
        self.btn_cam_y_neg.pressed.connect(on_press_cam_y_neg)
        self.btn_cam_y_neg.released.connect(timer_cam_y_neg.stop)

        self.btn_cam_z_pos = QPushButton()
        timer_cam_z_pos = QTimer()
        timer_cam_z_pos.timeout.connect(lambda: move_camera(dz=10))
        def on_press_cam_z_pos():
            move_camera(dz=10)
            timer_cam_z_pos.start(100)
        self.btn_cam_z_pos.pressed.connect(on_press_cam_z_pos)
        self.btn_cam_z_pos.released.connect(timer_cam_z_pos.stop)

        self.btn_cam_z_neg = QPushButton()
        timer_cam_z_neg = QTimer()
        timer_cam_z_neg.timeout.connect(lambda: move_camera(dz=-10))
        def on_press_cam_z_neg():
            move_camera(dz=-10)
            timer_cam_z_neg.start(100)
        self.btn_cam_z_neg.pressed.connect(on_press_cam_z_neg)
        self.btn_cam_z_neg.released.connect(timer_cam_z_neg.stop)

        main_layout.addWidget(self.btn_cam_x_pos)
        main_layout.addWidget(self.btn_cam_x_neg)
        main_layout.addWidget(self.btn_cam_y_pos)
        main_layout.addWidget(self.btn_cam_y_neg)
        main_layout.addWidget(self.btn_cam_z_pos)
        main_layout.addWidget(self.btn_cam_z_neg)

        self.btn_cam_left = QPushButton()
        timer_cam_left = QTimer()
        timer_cam_left.timeout.connect(lambda: rotate_camera('left'))
        def on_press_cam_left():
            rotate_camera('left')
            timer_cam_left.start(100)
        self.btn_cam_left.pressed.connect(on_press_cam_left)
        self.btn_cam_left.released.connect(timer_cam_left.stop)

        self.btn_cam_right = QPushButton()
        timer_cam_right = QTimer()
        timer_cam_right.timeout.connect(lambda: rotate_camera('right'))
        def on_press_cam_right():
            rotate_camera('right')
            timer_cam_right.start(100)
        self.btn_cam_right.pressed.connect(on_press_cam_right)
        self.btn_cam_right.released.connect(timer_cam_right.stop)

        self.btn_cam_up = QPushButton()
        timer_cam_up = QTimer()
        timer_cam_up.timeout.connect(lambda: rotate_camera('up'))
        def on_press_cam_up():
            rotate_camera('up')
            timer_cam_up.start(100)
        self.btn_cam_up.pressed.connect(on_press_cam_up)
        self.btn_cam_up.released.connect(timer_cam_up.stop)

        self.btn_cam_down = QPushButton()
        timer_cam_down = QTimer()
        timer_cam_down.timeout.connect(lambda: rotate_camera('down'))
        def on_press_cam_down():
            rotate_camera('down')
            timer_cam_down.start(100)
        self.btn_cam_down.pressed.connect(on_press_cam_down)
        self.btn_cam_down.released.connect(timer_cam_down.stop)

        main_layout.addWidget(self.btn_cam_left)
        main_layout.addWidget(self.btn_cam_right)
        main_layout.addWidget(self.btn_cam_up)
        main_layout.addWidget(self.btn_cam_down)

        self.btn_reset = QPushButton()
        self.btn_reset.clicked.connect(reset_camera)
        main_layout.addWidget(self.btn_reset)

        self.setLayout(main_layout)
        self.refresh_ui_texts()

    def refresh_ui_texts(self):
        self.setWindowTitle(tr("window_camera_title"))
        self.btn_cam_x_pos.setText(tr("cam_x_pos"))
        self.btn_cam_x_neg.setText(tr("cam_x_neg"))
        self.btn_cam_y_pos.setText(tr("cam_y_pos"))
        self.btn_cam_y_neg.setText(tr("cam_y_neg"))
        self.btn_cam_z_pos.setText(tr("cam_z_pos"))
        self.btn_cam_z_neg.setText(tr("cam_z_neg"))
        self.btn_cam_left.setText(tr("cam_left"))
        self.btn_cam_right.setText(tr("cam_right"))
        self.btn_cam_up.setText(tr("cam_up"))
        self.btn_cam_down.setText(tr("cam_down"))
        self.btn_reset.setText(tr("cam_reset"))

    def print_camera_state(self):
        cam = self.plotter.camera
        pos = cam.position
        focal = cam.focal_point
        az = cam.azimuth
        el = cam.elevation
        print(tr("camera_header"))
        print(tr("camera_position", pos=pos))
        print(tr("camera_focal", focal=focal))
        print(tr("camera_angles", az=az, el=el))
        print(tr("camera_footer"))

# ----------------------------------------
#  CRIANDO JANELAS E INICIANDO APLICAÇÃO
# ----------------------------------------
control_window = ControlWindow()
control_window.show()

camera_window = CameraControlWindow(plotter)
camera_window.show()

plotter.iren.add_observer("LeftButtonPressEvent", on_left_click)
plotter.iren.add_observer("KeyPressEvent", move_preview)
plotter.iren.add_observer("KeyPressEvent", capture_key_events)

plotter.show()
app.exec_()


