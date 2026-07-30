# Abaqus Random Cuboid Generator

A Python-based framework for generating randomly oriented, non-overlapping cuboids inside a three-dimensional box and automatically creating the corresponding Abaqus model with cuboid-shaped cutouts.

This project combines computational geometry algorithms with Abaqus scripting to generate reproducible finite element geometries containing randomly distributed cuboid regions.

The code is designed for applications such as:

- Stochastic geometry generation
- Representative Volume Element (RVE) modeling
- Porous material and void generation
- Random defect/inclusion distribution studies
- Abaqus automation workflows


## Example Generated Model

An example of the generated Abaqus geometry is shown below:

![Generated Abaqus Model](images/generated_model.png)


# Features

- Automatic generation of randomly positioned cuboids in 3D
- Random orientation using ZXZ Euler angles
- Uniform sampling of 3D rotations
- Non-overlapping cuboid placement
- Minimum clearance control between cuboids
- Minimum clearance control from box boundaries
- Separating Axis Theorem (SAT)-based collision detection
- Automatic Abaqus geometry creation
- Boolean cutting of cuboid regions from a box
- Reproducible results using user-defined random seeds
- Modular Python architecture


# Repository Structure

```
abaqus-random-cuboid-generator/

│
├── main.py
│   └── Main execution script
│
├── parameters.py
│   └── User-defined model parameters
│
├── generate_cuboids.py
│   └── Random cuboid generation algorithm
│
├── generate_model.py
│   └── Abaqus model construction and Boolean cutting
│
├── cuboids_intersection.py
│   └── SAT-based intersection and clearance checking
│
├── cuboids_vertices.py
│   └── 3D cuboid vertex calculation
│
├── rotation_matrix_zxz.py
│   └── ZXZ Euler rotation matrix calculation
│
├── README.md
│   └── Project documentation
│
├── LICENSE
│   └── MIT License
│
└── images/
    └── generated_model.png
        └── Example Abaqus model screenshot
```


# Requirements

- Abaqus/CAE with Python scripting support
- Abaqus Python environment
- NumPy available in the Abaqus Python environment

The script is intended to be executed using Abaqus/CAE.


# Running the Script

The script can be executed using either the Abaqus command line interface or the Abaqus/CAE graphical user interface.


## Method 1: Run Using Abaqus Command Line

Place all Python files in the same folder.

Open the Abaqus Command Prompt, navigate to the project folder, and run:

```bash
abaqus cae noGUI=main.py
```

Abaqus will execute the script without opening the graphical interface.


## Method 2: Run Using Abaqus/CAE GUI

The script can also be executed directly from Abaqus/CAE.

Steps:

1. Place all Python files in the same folder.

2. Open **Abaqus/CAE**.

3. From the menu bar select:

```
File → Run Script...
```

4. Browse to the project folder.

5. Select:

```
main.py
```

6. Click **OK**.

Abaqus will execute the script and generate the model automatically.


# Generated Model

After successful execution, Abaqus creates a model named:

```
GeneratedModel
```

The generated model contains:

- A three-dimensional rectangular box.
- Randomly oriented cuboid regions.
- A final geometry containing cuboid-shaped holes created using Boolean cutting.

The generated model can then be:

- inspected,
- modified,
- meshed,
- assigned materials,
- assigned loads and boundary conditions,
- analyzed using the standard Abaqus workflow.


# Configuration

All user-defined parameters are located in:

```
parameters.py
```

Example:

```python
config = {
    "BOX_DIMS": (60.0, 40.0, 50.0),
    "CUBOID_DIMS": (25.0, 15.0, 5.0),
    "NUM_CUBOIDS": 6,
    "MAX_ATTEMPTS": 100000,
    "RANDOM_SEED": 42,
    "MIN_CLEARANCE": 1.0,
}
```


## Parameters Description

| Parameter | Description |
|---|---|
| `BOX_DIMS` | Dimensions of the containing 3D box (X,Y,Z) |
| `CUBOID_DIMS` | Dimensions of each cuboid (length, width, thickness) |
| `NUM_CUBOIDS` | Number of cuboids to generate |
| `MAX_ATTEMPTS` | Maximum random placement attempts |
| `RANDOM_SEED` | Seed for reproducible geometry generation |
| `MIN_CLEARANCE` | Minimum allowed distance between objects |


# Algorithm Description

The geometry generation process consists of four main steps.


## 1. Random Orientation Generation

Each cuboid is assigned a random three-dimensional orientation using ZXZ Euler angles:

- Alpha rotation around global Z-axis
- Beta rotation around global X-axis
- Gamma rotation around global Z-axis

The rotation matrix is calculated in:

```
rotation_matrix_zxz.py
```


## 2. Cuboid Vertex Transformation

Each cuboid is initially defined in its local coordinate system.

The local coordinates are transformed into global coordinates using:

```
cuboids_vertices.py
```


## 3. Collision and Clearance Detection

The project uses the Separating Axis Theorem (SAT) to determine whether two cuboids violate the required spacing.

Implemented in:

```
cuboids_intersection.py
```

The algorithm considers:

- Cuboid structural axes
- Cross products between cuboid edges
- Numerical tolerance handling


## 4. Abaqus Model Generation

After valid cuboid configurations are generated, the cuboids are merged and used to cut regions from the main box.

Implemented in:

```
generate_model.py
```

The final geometry is created using Abaqus Boolean Cut operations.


# Workflow

```
Modify parameters.py
        |
        ↓
Run main.py in Abaqus
        |
        ↓
Generate random cuboid positions and orientations
        |
        ↓
Check intersection and clearance conditions
        |
        ↓
Merge valid cuboids
        |
        ↓
Perform Boolean cut in Abaqus
        |
        ↓
Continue with finite element modelling
```


# Reproducibility

The generated geometry can be reproduced by keeping the same:

- Random seed
- Box dimensions
- Cuboid dimensions
- Number of cuboids
- Clearance requirements


# Future Improvements

Possible future extensions:

- Automatic material assignment
- Automatic mesh generation
- Boundary condition generation
- Abaqus job submission automation
- Post-processing tools
- Additional inclusion geometries
- Visualization utilities


# Author

**Ayad Al-Rumaithi**


# Citation

If you use this software in academic work, please cite it as:

```
Al-Rumaithi, A. (2026).
Abaqus Random Cuboid Generator.
GitHub repository.
```


# License

This project is licensed under the MIT License.

See the `LICENSE` file for details.


# Acknowledgements

This project uses:

- Abaqus Python scripting environment
- NumPy numerical computing library
- Separating Axis Theorem for geometric collision detection