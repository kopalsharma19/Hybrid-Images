The goal of this assignment is to write an image filtering function and use it to create hybrid images using a simplified version of the SIGGRAPH 2006 paper by Oliva, Torralba, and Schyns. Hybrid images are static images that change in interpretation as a function of the viewing distance. The basic idea is that high frequency tends to dominate perception when it is available, but, at a distance, only the low frequency (smooth) part of the signal can be seen. By blending the high frequency portion of one image with the low-frequency portion of another, you get a hybrid image that leads to different interpretations at different distances.

I used the images of the current prime minister of india, narendra modi and another indian politician, Rahul Gandhi. 
The dimension of both of the images was 400 x 400. 

The images are - 

![modi](https://github.com/kopalsharma19/Hybrid-Images/assets/43065428/22459a33-d5d8-4f8b-bbe7-4eb523226d20)

![rahul-gandhi (1)](https://github.com/kopalsharma19/Hybrid-Images/assets/43065428/2832b76b-b5d3-4621-9ae3-6d99475fa4bc)


The configurations of the hybrid image was - 

{

  "left_sigma": 1.7,

  "left_size": 13,

  "left_mode": "low",

  "right_sigma": 6.9,

  "right_size": 8,

  "right_mode": "high",

  "mixin_ratio": 0.5,

  "scale_factor": 1.4,

  "view_grayscale": 0,

  "save_grayscale": 0
  
}

The hybrid image is 

![modi-gandhi-hybrid](https://github.com/kopalsharma19/Hybrid-Images/assets/43065428/cd4b87bf-8467-4f54-a2d2-309a04f741d1)

I used low pass for the left and and high pass for the right image, trying to form a perfect blend where both can be recognized from different 
perspectives. 

To run this program - 
1. Go to the main directory in the anaconda prompt terminal
2. Create an environment.yml
3. Activate conda environment
4. run the code line "python gui.py -t resources/sample-correspondance.json -c resources/sample-config.json"
5. Load left image and right image manually in the GUI
6. View the hybrid image and adjust parameters to create the perfect blend
7. Save your hybrid image

Thanks! 

Contributor - Kopal Sharma (kopalsharma2000)


