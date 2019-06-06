class Constant:
    '''Used to classify constants identified in algebraic expressions.'''
    
    def __init__(self, value: (int, float)):
        if (isinstance(value, (int, float))):
            self.value = value
        else:
            raise TypeError('Constants must be given a number, not a '+str(type(value)))

    def __repr__(self) -> str:
        return 'Constant('+str(self.value)+')'

    def __str__(self) -> str:
        return str(self.value)

    def __lt__(self, other: 'Constant') ->bool:
        if isinstance(other, Constant):
            return self.value < other.value
        else:
            raise TypeError('Constants can only be compared to other Constants, not a '+str(type(other)))

    def __gt__(self, other: 'Constant') -> bool:
        if isinstance(other, Constant):
            return self.value > other.value
        else:
            raise TypeError('Constants can only be compared to other Constants, not a '+str(type(other)))

    def __eq__(self, other: 'Constant') -> bool:
        if isinstance(other, Constant):
            return self.value == other.value
        else:
            return False

    def __le__(self, other: 'Constant') -> bool:
        return self < other or self == other

    def __ge__(self, other: 'Constant') -> bool:
        return self > other or self == other

    def classify(parts: list) -> list:
        '''Clasifies numeric items in given parts as constants.'''
        if not isinstance(parts, list):
            raise TypeError('Constant.classify() only accepts list types, not '+type(parts)+' types')
        i = 0
        while i < len(parts):
            try:
                if parts[i].isdecimal():
                    parts[i] = Constant(float(parts[i]))
            except AttributeError:
                pass
            except:
                raise
            i += 1
        return parts

class Variable():
    '''Used to classify variables identified in algebraic expressions.'''
    
    def __init__(self, name: str):
        if isinstance(name, str):
            self.name = name
            return
        else:
            raise TypeError('Variables must have a string as their argument, not a '+str(type(name)))

    def __repr__(self) -> str:
        return 'Variable('+repr(self.name)+')'

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: 'Variable') -> bool:
        if isinstance(other, Variable):
            return self.name == other.name
        else:
            return False
        
    def classify(parts: list) -> list:
        '''Clasifies alphabetic items in given parts as variables.'''
        if not isinstance(parts, list):
            raise TypeError('Variable.classify() only accepts list types, not '+type(parts)+' types')
        i = 0
        while i < len(parts):
            try:
                if parts[i].isalnum():
                    parts[i] = Variable(str(parts[i]))
            except AttributeError:
                pass
            except:
                raise
            i += 1
        return parts

class Operation():
    '''Base class for algebraic operation classes.'''

    symbol = NotImplemented

    def __init__(self, *parts: (Constant, Variable, 'Operation')):
        if len(parts) < 2:
            raise TypeError('Operations must have at least two parts, not '+str(len(parts)))
        i = 0
        while i < len(parts):
            if not isinstance(parts[i], (Constant, Variable, Operation)):
                raise TypeError('Every part of an operation must be either a Constant, a Variable, or an Operation not a '+str(type(parts[i]))+' at index '+str(i))
            i += 1
        self.parts = list(parts)
        return

    def __repr__(self) -> str:
        raise NotImplementedError('__repr__ should be overridded by derivitive classes')

    def __str__(self) -> str:
        raise NotImplementedError('__str__ should be overridded by derivitive classes')

    def __eq__(self, other: 'Operation') -> bool:
        if not isinstance(other, Operation):
            return False
        if type(self) != type(other):
            return False
        if len(self.parts) != len(other.parts):
            return False
        i = 0
        while i < len(self.parts):
            value = self.parts[i]
            if self.parts.count(value) != other.parts.count(value):
                return False
            i += 1
        else:
            return True

    def evaluate(self, lhs_i: int, rhs_i: int) -> ('Operation', Constant):
        raise NotImplementedError('evaluate() should be overridden by derivitive classes')
    
    def classify(subclass, *parts: (str, Constant, Variable)) -> ('Operation', list):
        if not issubclass(subclass, Operation):
            raise TypeError('Operation.classify() subclass argument must be a derivitive class of Operation, not '+subclass.__bases__)
        if subclass.symbol == NotImplemented:
            raise NotImplementedError('Operation.symbol should be overridden in derivitive classes to use Operation.classify()')
        parts = list(parts)
        i = 0
        while i < len(parts):
            part = parts.pop(i)
            if part == subclass.symbol:
                try:
                    i -= 1
                    lhs = parts.pop(i)
                    rhs = parts.pop(i)
                except IndexError:
                    raise ValueError('Impossible equation')
                except:
                    raise
                args = []
                if isinstance(lhs, subclass):
                    for part in lhs.parts:
                        args.append(part)
                else:
                    args.append(lhs)
                if isinstance(rhs, subclass):
                    for part in rhs.parts:
                        args.append(part)
                else:
                    args.append(rhs)
                try:
                    parts.insert(i, subclass(*args))
                    subclass.classify(parts)
                    i += 1
                except TypeError:
                    parts.insert(i, rhs)
                    parts.insert(i, part)
                    parts.insert(i, lhs)
                    i += 2
                except:
                    raise
                
            else:
                parts.insert(i, part)
                i += 1
        if len(parts) == 1:
            return parts[0]
        else:
            return parts

class Sum(Operation):
    '''Used for representing addition in algebraic expressions.'''

    symbol = '+'
    
    def __repr__(self) -> str:
        rep = 'Sum('
        for part in self.parts:
            rep += repr(part)+','
        return rep[0:-1]+')'

    def __str__(self) -> str:
        string = '('
        for part in self.parts:
            string += str(part)+' + '
        return string[0:-3]+')'

    def evaluate(self, lhs_i: int, rhs_i: int) ->('Sum', Constant):
        if not isinstance(self.parts[lhs_i], Constant):
            raise TypeError('Part at left hand side index must be a Constant to evalute, not a '+str(type(self.parts[lhs_i])))
        if not isinstance(self.parts[rhs_i], Constant):
            raise TypeError('Part at right hand side index must be a Constant to evaluate, not a '+str(type(self.parts[rhs_i])))
        value = self.parts[lhs_i].value + self.parts[rhs_i].value
        if len(self.parts) == 2:
            return Constant(value)
        else:
            self.parts[lhs_i] = Constant(value)
            self.parts.pop(rhs_i)
            return self

    def classify(*parts: (str, Constant, Variable, Operation)) -> ('Sum', list):
        return Operation.classify(__class__, *parts)

class Product(Operation):
    '''Used to represent muliplication in algebraic expressions.'''

    symbol = '*'
    
    def __repr__(self) -> str:
        rep = 'Product('
        for part in self.parts:
            rep += repr(part)+','
        return rep[0:-1]+')'

    def __str__(self) -> str:
        string = '('
        for part in self.parts:
            string += str(part)+' * '
        return string[0:-3]+')'

    def evaluate(self, lhs_i: int, rhs_i: int) -> ('Product', Constant):
        if not isinstance(self.parts[lhs_i], Constant):
            raise TypeError('Part at left hand side index must be a Constant to evalute')
        if not isinstance(self.parts[rhs_i], Constant):
            raise TypeError('Part at right hand side index must be a Constant to evaluate.')
        value = self.parts[lhs_i].value * self.parts[rhs_i].value
        if len(self.parts) == 2:
            return Constant(value)
        else:
            self.parts[lhs_i] = Constant(value)
            self.parts.pop(rhs_i)
            return self

    def classify(*parts: (str, Constant, Variable, Operation)) -> ('Product', list):
        return Operation.classify(__class__, *parts)

class Equation():
    '''Used as a base class for equations.'''

    symbol = NotImplemented
    
    def __init__(self, lhs: (Operation, Variable, Constant), rhs: (Operation, Variable, Constant)) -> 'Equation':
        if not isinstance(lhs, (Operation, Variable, Constant)):
            raise TypeError('Equation left hand side must be an Operation, a Variable, or a Constant')
        if not isinstance(rhs, (Operation, Variable, Constant)):
            raise TypeError('Equation right hand side must be an Operation, a Variable, or a Constant')
        self.lhs = lhs
        self.rhs = rhs
        return
    
    def __repr__(self) -> str:
        raise NotImplemented('Equation.__repr__() should be defined in derivitive class')

    def __str__(self) -> str:
        raise NotImplemented('Equation__str__() should be defined in derivitive class')

    def __eq__(self, other):
        if not isinstance(other, Equation):
            return False
        return (type(self) == type(other)) and (self.lhs == other.lhs) and (self.rhs == other.rhs)

    def classify(subclass, *parts: (str, Constant, Variable, Operation)) -> ('Equation', list):
        if not issubclass(subclass, Equation):
            raise TypeError('Equation.classify() subclass argument must be a derivitive class of Equation, not '+subclass.__bases__)
        if subclass.symbol == NotImplemented:
            raise NotImplementedError('Equation.symbol should be overridden in derivitive classes to use Equation.classify()')
        if len(parts) == 3 and parts[1] == subclass.symbol:
                try:
                    return subclass(parts[0],parts[2])
                except TypeError:
                    raise ValueError('Impossible equation')
                except:
                    raise
        else:
            return parts

class Equal(Equation):
    '''Used to represent equality equations.'''

    symbol = '='
    
    def __repr__(self) -> str:
        return 'Equal('+repr(self.lhs)+','+repr(self.rhs)+')'

    def __str__(self) -> str:
        return str(self.lhs)+' = '+str(self.rhs)

    def __eq__(self, other) -> bool:
        return Equation.__eq__(self, other) or (isinstance(other, Equal) and (self.lhs == other.rhs) and (self.rhs == other.lhs))

    def classify(*parts: (str, Constant, Variable, Operation)) -> ('Equal', list):
        return Equation.classify(__class__, *parts)

class Greater(Equation):
    '''Used to represent inequality equations where the left hand side is greater than the right hand side.'''

    symbol = '>'

    def __repr__(self) -> str:
        return 'Greater('+repr(self.lhs)+','+repr(self.rhs)+')'

    def __str__(self) ->str:
        return str(self.lhs)+' > '+str(self.rhs)

    def __eq__(self, other) -> bool:
        return Equation.__eq__(self, other) or (isinstance(other, Lesser) and (self.lhs == other.rhs) and (self.rhs == other.lhs))
    
    def classify(*parts: (str, Constant, Variable, Operation)) -> ('Greater', list):
        return Equation.classify(__class__, *parts)

class Lesser(Equation):
    '''Used to represent inequality equations where the left hand side is lesser than the right hand side.'''

    symbol = '<'

    def __repr__(self) -> str:
        return 'Lesser('+repr(self.lhs)+','+repr(self.rhs)+')'

    def __str__(self) -> str:
        return str(self.lhs)+' < '+str(self.rhs)

    def __eq__(self, other) -> bool:
        return Equation.__eq__(self, other) or (isinstance(other, Greater) and (self.lhs == other.rhs) and (self.rhs == other.lhs))
    
    def classify(*parts: (str, Constant, Variable, Operation)) -> ('Lesser', list):
        return Equation.classify(__class__, *parts)

class GreaterEqual(Equation):
    '''Used to represent inequality equations where the left hand side is greater than or equal to the right hand side.'''

    symbol = '>='

    def __repr__(self) -> str:
        return 'GreaterEqual('+repr(self.lhs)+','+repr(self.rhs)+')'

    def __str__(self) -> str:
        return str(self.lhs)+' >= '+str(self.rhs)

    def __eq__(self, other) -> bool:
        return Equation.__eq__(self, other) or (isinstance(other, LesserEqual) and (self.lhs == other.rhs) and (self.rhs == other.lhs))
    
    def classify(*parts: (str, Constant, Variable, Operation)) -> ('GreaterEqual', list):
        return Equation.classify(__class__, *parts)

class LesserEqual(Equation):
    '''Used to represent inequality equations where the left hand side is lesser thn or equal to the right hand side.'''

    symbol = '<='

    def __repr__(self) -> str:
        return 'LesserEqual('+repr(self.lhs)+','+repr(self.rhs)+')'

    def __str__(self) -> str:
        return str(self.lhs)+' <= '+str(self.rhs)

    def __eq__(self, other) -> bool:
        return Equation.__eq__(self, other) or (isinstance(other, GreaterEqual) and (self.lhs == other.rhs) and (self.rhs == other.lhs))
    
    def classify(*parts: (str, Constant, Variable, Operation)) -> ('LesserEqual', list):
        return Equation.classify(__class__, *parts)

class NotEqual(Equation):
    '''Used to represent inequalities where the left hand side is not equal to the right hand side.'''

    symbol = '!='

    def __repr__(self) -> str:
        return 'NotEqual('+repr(self.lhs)+','+repr(self.rhs)+')'

    def __str__(self) -> str:
        return str(self.lhs)+' != '+str(self.rhs)

    def __eq__(self, other) -> bool:
        return Equation.__eq__(self, other) or (isinstance(other, NotEqual) and (self.lhs == other.rhs) and (self.rhs == other.lhs))
    
    def classify(*parts: (str, Constant, Variable, Operation)) -> ('NotEqual', list):
        return Equation.classify(__class__, *parts)

#Constant tests
assert Constant(5).value==5
assert repr(Constant(5))=='Constant(5)'
assert str(Constant(5))=='5'
assert Constant(5)>Constant(4)
assert Constant(4)<Constant(5)
assert Constant(3.4)==Constant(3.4)
assert Constant(2.0)<=Constant(2)
assert Constant(23)>=Constant(5.6)
assert Constant(-3)!=Constant(7/2)
assert Constant.classify(['12','=','3','*','x'])==[Constant(12),'=',Constant(3),'*','x']

#Variable tests
assert Variable('x').name=='x'
assert repr(Variable('x'))=='Variable(\'x\')'
assert str(Variable('c'))=='c'
assert Variable('sd')==Variable('sd')
assert Variable('er')!=Variable('speed')
assert Variable.classify([Constant(12),'=',Constant(3),'*','x'])==[Constant(12),'=',Constant(3),'*',Variable('x')]

#Operation tests
assert Operation(Constant(5),Variable('x')).parts==[Constant(5),Variable('x')]
assert Operation(Constant(4),Variable('r'),Operation(Constant(6),Variable('x')))==Operation(Constant(4),Variable('r'),Operation(Constant(6),Variable('x')))

#Sum tests
assert repr(Sum(Constant(5),Variable('x')))=='Sum(Constant(5),Variable(\'x\'))'
assert str(Sum(Constant(5),Variable('x')))=='(5 + x)'
assert Sum(Constant(5),Constant(4)).evaluate(0,1)==Constant(9)
assert Sum(Constant(5),Variable('x'),Constant(4)).evaluate(0,2)==Sum(Constant(9),Variable('x'))
assert Sum.classify(Constant(1),Sum.symbol,Constant(2),Sum.symbol,Variable('x'))==Sum(Constant(1),Constant(2),Variable('x'))

#Product tests
assert repr(Product(Constant(5),Variable('x')))=='Product(Constant(5),Variable(\'x\'))'
assert str(Product(Constant(5),Variable('x')))=='(5 * x)'
assert Product(Constant(5),Constant(4)).evaluate(1,0)==Constant(20)
assert Product(Constant(5),Variable('x'),Constant(4)).evaluate(2,0)==Product(Variable('x'),Constant(20))
assert Product.classify(Constant(1),Product.symbol,Constant(2),Product.symbol,Variable('x'))==Product(Constant(1),Constant(2),Variable('x'))

#Equation tests
assert Equation(Variable('velocity'),Variable('t')).lhs==Variable('velocity')
assert Equation(Constant(3.456),Constant(127)).rhs==Constant(127)
assert Equation(Constant(5),Variable('x'))==Equation(Constant(5),Variable('x'))

#Equal tests
assert repr(Equal(Variable('x'),Constant(5)))=='Equal(Variable(\'x\'),Constant(5))'
assert str(Equal(Constant(12.78),Constant(45)))=='12.78 = 45'
assert Equal(Constant(5),Variable('f'))==Equal(Variable('f'),Constant(5))
assert Equal(Constant(78),Sum(Constant(3),Variable('y')))==Equal(Constant(78),Sum(Constant(3),Variable('y')))
assert Equal.classify(Variable('x'),Equal.symbol,Constant(5))==Equal(Variable('x'),Constant(5))

#Greater tests
assert repr(Greater(Constant(7),Variable('d')))=='Greater(Constant(7),Variable(\'d\'))'
assert str(Greater(Variable('speed'),Constant(89)))=='speed > 89'
assert Greater(Variable('x'),Constant(5))==Lesser(Constant(5),Variable('x'))
assert Greater.classify(Variable('y'),Greater.symbol,Sum(Constant(3),Constant(4)))==Greater(Variable('y'),Sum(Constant(3),Constant(4)))

#Lesser tests
assert repr(Lesser(Constant(3.4),Product(Constant(5),Variable('x'))))=='Lesser(Constant(3.4),Product(Constant(5),Variable(\'x\')))'
assert str(Lesser(Product(Variable('x'),Constant(90),Variable('y')),Constant(120.45)))=='(x * 90 * y) < 120.45'
assert Lesser(Sum(Variable('x'),Constant(7)),Product(Constant(8),Constant(23)))==Lesser(Sum(Variable('x'),Constant(7)),Product(Constant(8),Constant(23)))
assert Lesser(Product(Variable('x'),Sum(Constant(34),Variable('x'))),Constant(45))==Greater(Constant(45),Product(Variable('x'),Sum(Constant(34),Variable('x'))))
assert Lesser.classify(Constant(5),Lesser.symbol,Sum(Constant(3),Constant(2)))==Lesser(Constant(5),Sum(Constant(3),Constant(2)))

#GreaterEqual tests
assert repr(GreaterEqual(Variable('x'),Constant(5)))=='GreaterEqual(Variable(\'x\'),Constant(5))'
assert str(GreaterEqual(Sum(Constant(56),Variable('oxygen'),Constant(3.41)),Variable('hydrogen')))=='(56 + oxygen + 3.41) >= hydrogen'
assert GreaterEqual(Variable('x'),Product(Variable('x'),Constant(56)))==GreaterEqual(Variable('x'),Product(Variable('x'),Constant(56)))
assert GreaterEqual(Sum(Variable('x'),Constant(5)),Constant(5))==LesserEqual(Constant(5),Sum(Constant(5),Variable('x')))
assert GreaterEqual.classify(Sum(Constant(5),Variable('x')),GreaterEqual.symbol,Product(Variable('y'),Constant(1)))==GreaterEqual(Sum(Constant(5),Variable('x')),Product(Variable('y'),Constant(1)))

#LesserEqual tests
assert repr(LesserEqual(Constant(5),Constant(5)))=='LesserEqual(Constant(5),Constant(5))'
assert str(LesserEqual(Variable('x'),Product(Variable('x'),Constant(56),Constant(3.4))))=='x <= (x * 56 * 3.4)'
assert LesserEqual(Variable('dx'),Variable('dy'))==LesserEqual(Variable('dx'),Variable('dy'))
assert LesserEqual(Sum(Variable('f'),Variable('g')),Constant(7))==GreaterEqual(Constant(7),Sum(Variable('f'),Variable('g')))
assert LesserEqual.classify(Variable('speed'),LesserEqual.symbol,Constant(100))==LesserEqual(Variable('speed'),Constant(100))

#NotEqual tests
assert repr(NotEqual(Constant(4),Variable('t')))=='NotEqual(Constant(4),Variable(\'t\'))'
assert str(NotEqual(Constant(3),Sum(Variable('x'),Variable('y'))))=='3 != (x + y)'
assert NotEqual(Variable('f'),Product(Constant(4),Constant(4)))==NotEqual(Variable('f'),Product(Constant(4),Constant(4)))
assert NotEqual(Sum(Variable('x'),Variable('y'),Variable('z')),Product(Constant(34),Constant(56)))==NotEqual(Product(Constant(56),Constant(34)),Sum(Variable('y'),Variable('z'),Variable('x')))
assert NotEqual.classify(Constant(5),NotEqual.symbol,Product(Variable('f'),Variable('g')))==NotEqual(Constant(5),Product(Variable('f'),Variable('g')))
