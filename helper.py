import numpy as np
import cv2

def create_K(width_current=None,height_current=None):
    """
    Si 'width_current' et 'height_current' ne sont pas nulles, ils sont utilisés pour adapter 
    la matrice K par rapport à une image courante dont la taille peut différer de l'image de 
    référence (width_ref, height_ref) utilisée pour l'étalonnage (par exemple, une taille plus petite). 
    Cela permet de créer la matrice K en utilisant les dimensions de l'image courante : 
    create_K(image_current.shape[1], image_current.shape[0]).
    """
    #SIZE OF REFERENCE IMAGE
    width_ref=960
    height_ref=540
    #CONNAISSANCE DE LA GEOMETRIE D'ACQUISITION
    dX=155.0 #mm
    dY=105.0 #mm
    dZ=500.0 #mm
    #CONNAISSANCE DES DIMENSIONS EN PIXELS DANS L'IMAGE NUMERIQUE
    dx=243.0 #pixels
    dy=170.0 #pixels
    #CALCULS
    x_0=width_ref/2.0
    y_0=height_ref/2.0
    alpha_x=dx*dZ/dX
    alpha_y=dy*dZ/dY
    #IF CURRENT IMAGE HAS A DIFFERENT SIZE
    if width_current is not None:
        x_0=width_current/2.0
        alpha_x=alpha_x*width_current/float(width_ref)
    if height_current is not None:
        y_0=height_current/2.0
        alpha_y=alpha_y*height_current/float(height_ref)
    #MATRICE INTRINSEQUE
    K=np.zeros((3,3))
    K[0,0]=alpha_x
    K[1,1]=alpha_y
    K[0,2]=x_0
    K[1,2]=y_0
    K[2,2]=1
    return K

def pixels2camera(pixel_coords, K, Z):
    '''
    Sans cas "len(pixel_coords.shape) == 1", il faut
    invoke : one_point_3d=helper.pixels2camera(np.array([one_point_2d]),K,Z=10)[0]
    '''
    cammm_coords = None
    #Case list of pixels (one pixel per row)
    if len(pixel_coords.shape) == 2 :
        #ETAPE 1: (x,y) -> (x,y,1) (coordonnees homogenes)
        vecteur_colonne_unitaire=np.ones((pixel_coords.shape[0], 1)) #Vecteur colonne de 1
        pixel_coords_h=np.hstack((pixel_coords, vecteur_colonne_unitaire)) #Ajout de la colonne
        #ETAPE 2: (x,y,1) -> Z*(x,y,1)=(Zx,Zy,Z)=(x',y',z') 
        pixel_coords_h_Z = Z * pixel_coords_h
        #ETAPE 3: inversion de K
        K_inv=np.linalg.inv(K)
        #ETAPE 4: produit matriciel
        cammm_coords=np.dot(K_inv,pixel_coords_h_Z.T).T
    #Case list of pixels (one pixel per row)
    elif len(pixel_coords.shape) == 1 :
        #ETAPE 1: (x,y) -> (x,y,1) (coordonnees homogenes)
        vecteur_colonne_unitaire=np.ones((1)) #Vecteur colonne de 1
        pixel_coords_h=np.hstack((pixel_coords,vecteur_colonne_unitaire)) #Ajout de la colonne
        #ETAPE 2: (x,y,1) -> Z*(x,y,1)=(Zx,Zy,Z)=(x',y',z') 
        pixel_coords_h_Z = Z * pixel_coords_h
        #ETAPE 3: inversion de K
        K_inv=np.linalg.inv(K)
        #ETAPE 4: produit matriciel
        cammm_coords=np.dot(K_inv,pixel_coords_h_Z)
         
    return cammm_coords

def camera2pixels(camera_coords,K):
    if  len(camera_coords.shape) == 2 :
        #ETAPE 1: projection par produit matriciel -> coordonnees homogenes
        pixel_coords_h=np.dot(K, camera_coords.T).T
        #ETAPE 2: normalisation, pour chaque ligne (point x,y,z), on divise par le dernier terme (z) 
        #Remarque: on travaille sur l'ensemble des points (lignes) a chaque etape (optimisation)
        pixel_coords_h[:, 0] = pixel_coords_h[:, 0] / pixel_coords_h[:, 2]
        pixel_coords_h[:, 1] = pixel_coords_h[:, 1] / pixel_coords_h[:, 2]
        pixel_coords_h[:, 2] = pixel_coords_h[:, 2] / pixel_coords_h[:, 2]
        #ETAPE 3: on ne conserve que les 2 premieres coordonnees (x et y)
        pixel_coords=pixel_coords_h[:, 0:2].astype(np.float32) #float32 sinon probleme avec drawChessboardCorners
    else: assert False, "Error in camera2pixels shape"
    return pixel_coords

def create_square(cords_pixel,size):
    """
    Dans cette fonction, on va calculer le centre de la carte de damier
    à partir des valeurs des pixels pris par la fonction 
    findChessboardCorners()
    cette fonction va généralement prendre comme paramétre
    square = create_square(corners2d, size) ou size est l'arrêt du carré
    """
    center=np.mean(cords_pixel,0)
    square = np.float32([[center[0]-0.5*size, center[1]-0.5*size], 
                         [center[0]+0.5*size, center[1]-0.5*size], 
                         [center[0]+0.5*size, center[1]+0.5*size], 
                         [center[0]-0.5*size, center[1]+0.5*size]])
    return square



def compute_extrinsic_matrix(pts3d,pts2d,K,verbose=False):
    dist_coef = np.zeros(4)

    retval,rvec,tvec=cv2.solvePnP(pts3d, pts2d, K, dist_coef)
    """
    — la fonction solvePnP requiert les distorsions :on utilisera dist=np.zeros(4) 
      afin de supposer qu’aucune distorsion n’est présente.
    — la fonction solvePnP retourne les angles de rotation (selon les axes X, Y et Z) que
      l’on pourra afficher (print) pour comparer avec l’estimation manuelle. Attention à la
      conversion degré en radians.
    — la fonction solvePnP retourne les angles de rotation que l’on pourra exprimer sous forme
      matricielle (matrice 3x3) à l’aide de la fonction opencv Rodrigues : R,b=cv2.Rodrigues
      (rvec). En ajoutant le vecteur de translation (retourné par solvePnP) à cette matrice
      3x3, on obtiendra la matrice extrinsèque finale de taille 3x4 (la colonne de translation :
      M_ext=np.hstack((R,tvec))

    """
    R,b=cv2.Rodrigues(rvec)
    M_ext=np.hstack((R,tvec))
    if verbose:
        print ("Rotation x (deg): " , np.round(rvec[0]*360.0/(2*np.pi),2))
        print ("Rotation y (deg): " , np.round(rvec[1]*360.0/(2*np.pi),2))
        print ("Rotation z (deg): " , np.round(rvec[2]*360.0/(2*np.pi),2))
        print ("Translation: ",np.round(tvec[0],2), ", " , np.round(tvec[1],2), ", "  , np.round(tvec[2],2))
        
        np.set_printoptions(suppress=True)
        print( "Matrice:\n", np.round(M_ext,2))
    return M_ext



