import random
import pyglet
from pyglet.gl import *
import numpy as np
import pickle

class main (pyglet.window.Window):
    def __init__ (self):
        super(main, self).__init__(20, 20, fullscreen = False)
        self.square = Square(self.width/4, self.height/4, self.width/2, self.height/2, self)
        self.alive = 1

    def on_close(self):
        self.alive = 0

    def on_key_press(self, symbol, modifiers):
        if symbol == 65307: # [ESC]
            self.alive = 0

    def render(self):
        self.clear()
        glClearColor(0, 0.3, 0.5, 0)
        glClear(GL_COLOR_BUFFER_BIT)
        self.square.draw()
        self.flip()

    def save_window(self):
        pass

    def run(self):
        labels = []
        features = []
        for i in xrange(10):

            if self.alive == 0:
                break
        
            self.square.setRandomState()
            self.render()


            image_data = pyglet.image.get_buffer_manager().get_color_buffer().get_image_data()
            image = np.frombuffer(image_data.get_data("I",
                image_data.width),np.uint8).reshape((image_data.width,image_data.height))
            np.set_printoptions(threshold=np.inf)
            print(image)

            event = self.dispatch_events()
            labels.append ((self.square.xpos,self.square.ypos,self.square.angle))
            features.append(image)
        validation_fraction = 0.3
        partition = int(len(features)*validation_fraction)
        data = {"train":{},"valid":{}}
        data["train"]["features"] = features[partition:]
        data["train"]["labels"] = labels[partition:]
        data["valid"]["features"] = features[:partition]
        data["valid"]["labels"] = labels[:partition]
        pickle.dump(data, open("./data.pickle","wb"))

        #a = pickle.load(open("./data.pickle","rb"))

class Square:
    def __init__(self, width, height, xpos, ypos, window):
        self.xpos = xpos
        self.ypos = ypos
        self.angle = 0
        self.window = window
        self.size = 1
        x = width/2.0
        y = height/2.0
        self.vlist = pyglet.graphics.vertex_list(4, ('v2f', [-x,-y, x,-y, -x,y, x,y]), ('t2f', [0,0, 1,0, 0,1, 1,1]))
    def draw(self):
        glPushMatrix()
        glTranslatef(self.xpos, self.ypos, 0)
        glRotatef(self.angle, 0, 0, 1)
        glScalef(self.size, self.size, self.size)
        glColor3f(.1,1,1)
        self.vlist.draw(GL_TRIANGLE_STRIP)
        glPopMatrix()
    def setRandomState(self):
        self.xpos= random.uniform(0, self.window.width)
        self.ypos = random.uniform(0,self.window.width)
        self.angle =random.uniform(0, 359)

def get_data_point(window):
    pass


x = main()
x.run()
