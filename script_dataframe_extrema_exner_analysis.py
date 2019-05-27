from soma import aims
import numpy as np
import os
import csv

if __name__ == '__main__':
    lat_min = 85
    lat_max = 110
    lon_min = 5
    lon_max = 20
    nb_it_smooth = 10

    BV_database_path = '/home/mulaw/Documents/BV_Exner/enfantstri'
    mesh_path = 't1mri/default_acquisition/default_analysis/segmentation/mesh'
    lonlat_path ='surface_analysis'
    side ='L'
    rect_path = '/home/mulaw/Documents/BV_Exner/data_extrema/rectangles'
    ext_path = '/home/mulaw/Documents/BV_Exner/data_extrema/extrema'
    ab_path = '/home/mulaw/Documents/BV_Exner/data_extrema/scripts/data'
    dataframe = '/home/mulaw/Documents/BV_Exner/data_extrema/scripts/data'	#chemin d'enregistrement du fichier csv


    fres=open(dataframe+"/res_brainvisa_enfants.csv",'a+')			#Creation en mode ouverture du fichier fres
    fres.write('Subject ,nb_extrema, index,  val_extrema , Cord_x , Cord_y')	#Entete des colonnes du fichier
    
    subjects = list()
    subj_files_list=os.listdir(BV_database_path)
    for fil in subj_files_list:
        if fil.find('.') == -1:
            subjects.append(fil)
    print('subjects to be processed :')
    subjects_pb = list()
    subj_ext_values = list()
    subj_ext_coords = list()
    subj_ext_max_coords = list()
    subjects_processed = list()
   
    for subj in subjects:
        print('--processing subject '+subj)
        
        corresp_texture_file = os.path.join(rect_path, subj+'/', subj+'_'+side+'white_exner_rectangle_corresp.gii')
        rectangular_mesh_file = os.path.join(rect_path, subj+'/', subj+'_'+side+'white_exner_rectangle.gii')
        texture_extrema_file = os.path.join(ext_path,subj+'/', subj+'_'+side+'white_spmT_con_smooth_extrema.tex')

        try:
            # Lecture des fichiers 
            rectangular_mesh = aims.read(rectangular_mesh_file)
            extrema_tex = aims.read(texture_extrema_file)
            atex_ext = np.array(extrema_tex[0])
            corresp_tex = aims.read(corresp_texture_file)
            atex_corresp = np.array(corresp_tex[0])

            # Extraction des extrema dans le rectangle
            inds_rect = atex_corresp>0
            ext_in_rect = atex_ext[inds_rect]
            inds_ext_in_rect = ext_in_rect>0
            values_ext_in_rect = ext_in_rect[inds_ext_in_rect]			#Valeurs des extrema 
            m_ind = np.argmax(ext_in_rect)
          
           
            #Extraction des coordonnees
            coords_rect = np.array(rectangular_mesh.vertex())[inds_rect, :2]
            coords_ext_in_rect = coords_rect[inds_ext_in_rect, :]		#Coordonnees des extrema
            coords_max_ext_in_rect = coords_rect[m_ind, :]

            subj_ext_values.append(values_ext_in_rect)
            subj_ext_coords.append(coords_ext_in_rect)
            subj_ext_max_coords.append(coords_max_ext_in_rect)
            subjects_processed.append(subj)
            print('----done')

	    # Boucle retournant les valeurs recherchees dans le fichier fres
	    for i in range(len(values_ext_in_rect)):
                fres.write('\n'+str(subj)+ ',' + str(len(values_ext_in_rect)) + ',' + str(i+1) + ',' + str(values_ext_in_rect[i]) + ',' + str(coords_ext_in_rect[i][0]) + ',' + str(coords_ext_in_rect[i][1])+ ',' ) #Ecriture dans le fichier
	  
        except Exception as e:
            print('----error '+str(e))
            subjects_pb.append(subj)
    print('subjects not processed:')
    print(subjects_pb)
    fres.close()
