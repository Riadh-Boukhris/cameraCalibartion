import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def plot_cube(points3D):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Define cube faces
    cube_faces = [[0, 1, 3, 2],
                  [4, 5, 7, 6],
                  [0, 1, 5, 4],
                  [2, 3, 7, 6],
                  [1, 2, 6, 5],
                  [3, 0, 4, 7]] 

    # Define colors for each face of the cube
    colors = ['r', 'g', 'b', 'y', 'm', 'c']

    # Plot cube faces
    for i, face in enumerate(cube_faces):
        square = [points3D[face[j]] for j in range(4)]
        square = Poly3DCollection([square])
        square.set_color(colors[i])
        square.set_edgecolor('k')
        ax.add_collection3d(square)

    # Set plot limits to span the whole cube
    max_range = np.array([points3D[:,0].max()-points3D[:,0].min(), 
                          points3D[:,1].max()-points3D[:,1].min(), 
                          points3D[:,2].max()-points3D[:,2].min()]).max()
    mid_x = (points3D[:,0].max()+points3D[:,0].min()) * 0.5
    mid_y = (points3D[:,1].max()+points3D[:,1].min()) * 0.5
    mid_z = (points3D[:,2].max()+points3D[:,2].min()) * 0.5
    ax.set_xlim(mid_x - max_range * 0.5, mid_x + max_range * 0.5)
    ax.set_ylim(mid_y - max_range * 0.5, mid_y + max_range * 0.5)
    ax.set_zlim(mid_z - max_range * 0.5, mid_z + max_range * 0.5)

    # Set labels for x, y, and z axes
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    plt.show()


plot_cube()