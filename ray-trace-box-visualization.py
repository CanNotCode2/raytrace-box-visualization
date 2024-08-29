import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

def parse_vector(vector_str):
    origin_str, direction_str = vector_str.split('direction:')
    origin_str = origin_str.replace('origin:', '').strip()
    direction_str = direction_str.strip()

    origin = np.array([float(x) for x in origin_str.split(',')])
    direction = np.array([float(x) for x in direction_str.split(',')])

    return origin, direction

def parse_box(box_str):
    box_str = box_str.replace('SimpleCollisionBox', '').strip('{}')
    components = [comp.split('=')[1] for comp in box_str.split(',')]
    min_x, min_y, min_z, max_x, max_y, max_z = map(float, components[:6])

    return min_x, min_y, min_z, max_x, max_y, max_z

def draw_vector(ax, origin, direction, length=10, **kwargs):
    ax.quiver(
        origin[0], origin[1], origin[2],
        direction[0], direction[1], direction[2],
        length=length, **kwargs
    )

def draw_box(ax, min_x, min_y, min_z, max_x, max_y, max_z, **kwargs):
    r = [min_x, max_x]
    X, Y = np.meshgrid(r, r)
    ax.scatter([min_x, max_x], [min_y, max_y], [min_z, max_z], c='r')

    # Draw faces
    ax.add_collection3d(Poly3DCollection([
        list(zip([min_x, min_x, max_x, max_x], [min_y, max_y, max_y, min_y], [min_z, min_z, min_z, min_z])),
        list(zip([min_x, min_x, max_x, max_x], [min_y, max_y, max_y, min_y], [max_z, max_z, max_z, max_z])),
        list(zip([min_x, min_x, min_x, min_x], [min_y, min_y, max_y, max_y], [min_z, max_z, max_z, min_z])),
        list(zip([max_x, max_x, max_x, max_x], [min_y, min_y, max_y, max_y], [min_z, max_z, max_z, min_z])),
        list(zip([min_x, max_x, max_x, min_x], [min_y, min_y, min_y, min_y], [min_z, min_z, max_z, max_z])),
        list(zip([min_x, max_x, max_x, min_x], [max_y, max_y, max_y, max_y], [min_z, min_z, max_z, max_z]))
    ], **kwargs))

def main():
    vector_str = "origin: 234.94632132425156,6.27,292.58369401837393 direction: -0.10548005814118344,-0.07040894031524658,0.9919256235540885"
    box_str = "SimpleCollisionBox{minX=233.9998, minY=5.9998, minZ=294.9998, maxX=235.0002, maxY=7.0002, maxZ=296.0002, isFullBlock=true}"

    origin, direction = parse_vector(vector_str)
    min_x, min_y, min_z, max_x, max_y, max_z = parse_box(box_str)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    draw_vector(ax, origin, direction, color='blue')
    draw_box(ax, min_x, min_y, min_z, max_x, max_y, max_z, alpha=0.3, color='red')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    ax.set_xlim([min(min_x, origin[0]), max(max_x, origin[0] + direction[0]*10)])
    ax.set_ylim([min(min_y, origin[1]), max(max_y, origin[1] + direction[1]*10)])
    ax.set_zlim([min(min_z, origin[2]), max(max_z, origin[2] + direction[2]*10)])

    plt.show()

if __name__ == "__main__":
    main()
