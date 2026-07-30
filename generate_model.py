from abaqus import *
from abaqusConstants import *

def generate_model(config, cuboid_data):
    """
    Build an Abaqus model with a box containing cuboids.

    Parameters:
        config : dict
            Configuration dictionary containing box/cuboid dimensions
            and model specifications.
        cuboid_data : list of tuples (center, angles, vertices)
            Information about cuboids: center coordinates, Euler angles, vertices.
    """
    # Extract parameters from the config dictionary
    BOX_W, BOX_H, BOX_D = config["BOX_DIMS"]
    CUB_W, CUB_H, CUB_D = config["CUBOID_DIMS"]
    
    model_name = 'GeneratedModel'

    # Delete existing model if it exists
    if model_name in mdb.models:
        del mdb.models[model_name]

    model = mdb.Model(name=model_name)
    assembly = model.rootAssembly

    # Create the main box part
    sketch_box = model.ConstrainedSketch(name='__box__', sheetSize=200.0)
    sketch_box.rectangle((0.0, 0.0), (BOX_W, BOX_H))
    box_part = model.Part(name='Box', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    box_part.BaseSolidExtrude(sketch=sketch_box, depth=BOX_D)

    # Create base cuboid part (centered at origin)
    sketch_cub = model.ConstrainedSketch(name='__cub__', sheetSize=200.0)
    sketch_cub.rectangle((-CUB_W/2.0, -CUB_H/2.0), (CUB_W/2.0, CUB_H/2.0))
    base_cuboid = model.Part(name='BaseCuboid', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    base_cuboid.BaseSolidExtrude(sketch=sketch_cub, depth=CUB_D)

    inst_list = []

    # Create rotated/transformed cuboid instances
    for i, (center, angles, _) in enumerate(cuboid_data):
        alpha, beta, gamma = angles
        inst_name = f'Cuboid_{i+1:06d}'

        assembly.Instance(name=inst_name, part=base_cuboid, dependent=ON)

        # Apply translations and rotations in order: Z(alpha) → X(beta) → Z(gamma)
        assembly.translate(instanceList=(inst_name,), vector=(0, 0, -CUB_D/2.0))
        assembly.rotate(instanceList=(inst_name,), axisPoint=(0,0,0), axisDirection=(0,0,1), angle=alpha)
        assembly.rotate(instanceList=(inst_name,), axisPoint=(0,0,0), axisDirection=(1,0,0), angle=beta)
        assembly.rotate(instanceList=(inst_name,), axisPoint=(0,0,0), axisDirection=(0,0,1), angle=gamma)
        assembly.translate(instanceList=(inst_name,), vector=center)
        inst_list.append(assembly.instances[inst_name])

    # Merge all cuboids into a single part for cutting
    assembly.InstanceFromBooleanMerge(
        name='MergedCuboids',
        instances=tuple(inst_list),
        originalInstances=DELETE,
        domain=GEOMETRY
    )
    assembly.Instance(name='MergedCuboids-2', part=model.parts['MergedCuboids'], dependent=ON)

    # Create box instance and cut cuboid holes
    assembly.Instance(name='Box-1', part=box_part, dependent=ON)
    assembly.InstanceFromBooleanCut(
        name='Box_With_Holes',
        instanceToBeCut=assembly.instances['Box-1'],
        cuttingInstances=(assembly.instances['MergedCuboids-2'],),
        originalInstances=DELETE
    )
