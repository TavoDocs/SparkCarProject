import cv2


# read the images
img1 = cv2.imread('libre.png')
img2 = cv2.imread('ocupado.png')
img3 = cv2.imread('especial.png')
img4 = cv2.imread('vacio.png')
img5 = cv2.imread('wall.png')

# define a function for vertically
# concatenating images of the
# same size and horizontally
def concat_vh(list_2d):
	
	# return final image
	return cv2.vconcat([cv2.hconcat(list_h)
						for list_h in list_2d])
# image resizing
img1_s = cv2.resize(img1, dsize = (0,0),
					fx = 0.5, fy = 0.5)
img2_s = cv2.resize(img2, dsize = (0,0),
					fx = 0.5, fy = 0.5)
img3_s = cv2.resize(img3, dsize = (0,0),
					fx = 0.5, fy = 0.5)
img4_s = cv2.resize(img4, dsize = (0,0),
					fx = 0.5, fy = 0.5)
img5_s = cv2.resize(img5, dsize = (0,0),
					fx = 0.5, fy = 0.5)

Status_img_Est = [img1_s,img2_s, img3_s]

Status_img_Est

# Matriz del mapa del estacionamiento
img_tile = concat_vh([[Status_img_Est[Status_Est[0]], Status_img_Est[Status_Est[1]], Status_img_Est[Status_Est[2]], Status_img_Est[Status_Est[3]], Status_img_Est[Status_Est[4]], Status_img_Est[Status_Est[5]], Status_img_Est[Status_Est[6]], Status_img_Est[Status_Est[7]], Status_img_Est[Status_Est[8]], Status_img_Est[Status_Est[9]], Status_img_Est[Status_Est[10]], img5_s, img5_s, img5_s, img5_s, img5_s],
					  [img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s],
					  [img4_s, Status_img_Est[Status_Est[11]], Status_img_Est[Status_Est[12]], Status_img_Est[Status_Est[13]], Status_img_Est[Status_Est[14]], Status_img_Est[Status_Est[15]], Status_img_Est[Status_Est[16]], Status_img_Est[Status_Est[17]], Status_img_Est[Status_Est[18]], Status_img_Est[Status_Est[19]], Status_img_Est[Status_Est[20]], Status_img_Est[Status_Est[21]], Status_img_Est[Status_Est[22]], Status_img_Est[Status_Est[23]], Status_img_Est[Status_Est[24]], img4_s],
					  [img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s, img4_s],
					  [img4_s, Status_img_Est[Status_Est[25]], Status_img_Est[Status_Est[26]], Status_img_Est[Status_Est[27]], Status_img_Est[Status_Est[28]], Status_img_Est[Status_Est[29]], Status_img_Est[Status_Est[30]], Status_img_Est[Status_Est[31]], Status_img_Est[Status_Est[32]], Status_img_Est[Status_Est[33]], img5_s, img5_s, img5_s, img5_s, img5_s, img5_s]])
# Guarda como una imagen png el mapa 
cv2.imwrite('E1.jpg', img_tile)