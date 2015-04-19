import random
import time

import pygame
from pygame.font import Font

import assets
import colors

pygame.init()

class Enemy():

    level = 0
    equation = ''
    solution = {0}

    spawn = 0
    impact = 0

    def __init__(self, level):
        
        self.level = level
        
        self.solution, expressions = self.generate(level)
        random.shuffle(expressions)
        self.equation = ' = '.join(expressions)

        self.spawn = time.time()
        self.impact = self.spawn + self.getTime()

    def __str__(self):
        return '{}; x = {}'.format(self.equation, self.solution)

    '''
    Subclass and override

    Expected: {int} solution(s) and [str, str]
    expressions that equal each other
    NOTE: This is STATIC and should be called from
    the CLASS!
    '''
    @staticmethod
    def generate(level):
        raise ValueError('Subclass me')

    '''
    Subclass and override

    Expected: float representing the seconds
    needed to cross
    '''
    def getTime(self):
        raise ValueError('Override me')
    
    '''
    Subclass and override

    Expected: int representing the points
    recieved from solving
    '''
    def getValue(self):
        raise ValueError('Override me')

    '''
    Subclass and override

    Expected: int representing number of chips
    in the "pot" of selecting what number
    NOTE: This is STATIC and should be called
    from the CLASS!
    '''
    @staticmethod
    def getChance():
        raise ValueError('Override me')

    '''
    Subclass and override

    Expected: Surface representing that will
    be displayed on the interface representing
    the equation
    '''
    def getSurface(self):
        raise ValueError('Override me')

    '''
    Check if the player's input is right
    '''
    def isCorrect(self, sltns):
        try:
            return set(map(int, sltns.split())) == self.solution
        except:
            return False

    '''
    Find how far the equation is to the base
    '''
    def getProgress(self):
        return (time.time() - self.spawn) / (self.impact - self.spawn)
    
class Level1(Enemy):
    '''
    A simple equation
    Example: x + 4 = 9
    Begins spawning at level 1
    Stops spawning after level 3
    '''

    font = Font('freesansbold.ttf', 16)
    
    @staticmethod
    def generate(level):
        
        x = random.randint(-50, 50)
        b = random.randint(-50, 50)
        y = x + b
        
        b = strAdd(b)

        exps = ['x {}'.format(b), str(y)]

        return {x}, exps

    def getTime(self):

        return cap(-2 * self.level + 15, 5, None)

    def getValue(self):
        return 50

    @staticmethod
    def getChance(level):
        
        chance = -10 * (level - 1) + 100
        if level > 3:
            chance = 0
        return chance

    def getSurface(self):

        surf = assets.rocket1.copy()
        equation = self.font.render(self.equation, True, colors.white)
        surf.blit(equation, (55, 25))
        return surf

class Level2(Enemy):
    '''
    A slightly more complex equation
    Example: 3x + 2 = 5
    Begins spawning at level 1
    '''

    font = Font('freesansbold.ttf', 16)

    @staticmethod
    def generate(level):
        
        m, x, b, y = genL2()
        
        m = strCoeff(m)
        b = strAdd(b)
            
        exps = ['{} {}'.format(m, b), str(y)]

        return {x}, exps

    def getTime(self):

        return cap(-(self.level - 1) + 25, 0, None)

    def getValue(self):

        return 100

    @staticmethod
    def getChance(level):

        return 150

    def getSurface(self):

        surf = assets.rocket1.copy()
        equation = self.font.render(self.equation, True, colors.white)
        surf.blit(equation, (55, 25))
        return surf

class Level3(Enemy):
    '''
    A 'two-step' equation
    Example: 3x + 4 = 4x + 3
    Begins spawning at level 6
    '''

    font = Font('freesansbold.ttf', 14)

    @staticmethod
    def generate(level):
        
        m1, x, b1, y = genL2()

        m2 = random.randint(-10, 10)
        b2 = y - m2 * x
        
        m1 = strCoeff(m1)
        m2 = strCoeff(m2)
        b1 = strAdd(b1)
        b2 = strAdd(b2)

        exps = ['{} {}'.format(m1, b1), '{} {}'.format(m2, b2)]

        return {x}, exps

    def getTime(self):

        return cap(-self.level + 30, 15, None)

    def getValue(self):

        return 200

    @staticmethod
    def getChance(level):

        if level < 6:
            return 0
        return int(cap(5 * (level - 5), None, 150))

    def getSurface(self):

        surf = assets.rocket2.copy()
        equation = self.font.render(self.equation, True, colors.black)
        surf.blit(equation, (64, 25))
        return surf
        
class Level4(Enemy):
    '''
    A binomial factor pair
    Example: (3x + 2)(5x - 1) = 0
    Begins spawning at level 10
    '''

    font = Font('freesansbold.ttf', 16)

    @staticmethod
    def generate(level):
        
        m1, x1, b1, m2, x2, b2 = genL4()

        m1 = strCoeff(m1)
        m2 = strCoeff(m2)
        b1 = strAdd(b1)
        b2 = strAdd(b2)
        
        equation = '({}{})({}{})'.format(m1, b1, m2, b2)
        
        return {x1, x2}, [equation, '0']

    def getTime(self):

        return 30 * 0.95 ** (self.level - 15) + 10
    
    def getValue(self):

        return 500

    @staticmethod
    def getChance(level):

        if level < 10:
            return 0
        chance = 10 * 1.25 ** (level - 10)
        if chance > 200:
            chance = 200
            
        return int(chance)

    def getSurface(self):

        surf = assets.rocket3.copy()
        equation = self.font.render(self.equation, True, colors.white)
        surf.blit(equation, (125, 25))
        return surf

class Level5(Enemy):
    '''
    A trinomial
    Example: x^2 + 9x + 10 = -10
    Begins spawning at level 15
    '''

    font = Font('freesansbold.ttf', 18)

    @staticmethod
    def generate(level):

        b1 = random.randint(-12, 11)
        if b1 == 0:
            b1 = 12
        b2 = random.randint(-12, 11)
        if b2 == 0:
            b2 = 12

        b = b1 + b2
        c = b1 * b2
        
        b = strCoeffAdd(b)
        c = strAdd(c)
        
        return {b1, b2}, ['x^2{}{}'.format(b, c), '0']
    
    def getTime(self):

        return 25 * 0.95 ** (self.level - 15) + 20
        
    def getValue(self):

        return 750

    @staticmethod
    def getChance(level):
        if level < 15:
            return 0
        chance = 25 * 1.10 ** (level - 15)

        return int(chance)

    def getSurface(self):

        surf = assets.rocket3.copy()
        equation = self.font.render(self.equation, True, colors.white)
        surf.blit(equation, (125, 25))
        return surf


class SpawnHandler():

    level = 1
    enemies = []
    
    def __init__(self, *enemies):
        self.enemies = enemies

    def levelUp(self):
        self.level += 1

    def spawnchoices(self):
        chips = []
        for enemy in self.enemies:
            for chip in range(0, enemy.getChance(self.level)):
                chips.append(enemy)
        return chips

    def spawn(self):
        return random.choice(self.spawnchoices())(self.level)

def genL2():
    
    x = random.randint(-12, 11)
    if x == 0:
        x = 12
    
    m = random.randint(-10, 9)
    if m == 0:
        m = 10
        
    b = random.randint(-10, 9)
    if b == 0:
        b = 10
        
    y = m * x + b

    return m, x, b, y

def genL4():
    
    m1, x1, b1, y1 = genL2()
    m2, x2, b2, y2 = genL2()
    
    b1 = b1 - y1
    b2 = b2 - y2
    
    return m1, x1, b1, m2, x2, b2

def strCoeff(n):
    if n == -1:
        n = '-x'
    elif n == 0:
        n = ''
    elif n == 1:
        n = 'x'
    else:
        n = '{}x'.format(n)
    return n

def strCoeffAdd(n):
    if n == -1:
        n = '- x'
    elif n < 0:
        n = ' - {}x'.format(abs(n))
    elif n == 0:
        n = ''
    elif n == 1:
        n = ' + x'
    elif n > 1:
        n = ' + {}x'.format(n)
    return n

def strAdd(n):
    if n < 0:
        n = ' - {}'.format(abs(n))
    elif n == 0:
        n = ''
    elif n > 0:
        n = ' + {}'.format(n)
    return n

'''
Cap a number to be greater than min but less than max
Example: cap(20, 5, 10) = 10
It's best used if a mathematical function is put
in the place of n.
'''
def cap(n, min=None, max=None):
    if min != None and n < min:
        return min
    elif max != None and n > max:
        return max
    return n

def factorsOf(n):
    for i in range(1, n):
        if n % i == 0:
            yield i
    yield n
        
def main():
    pygame.init()
    e = Level5(1, (640, 480))
    d = pygame.display.set_mode((640, 480))
    while True:
        d.blit(e.getSurface(), (0, 128))
        pygame.display.update()
    
if __name__ == '__main__':
    main()
