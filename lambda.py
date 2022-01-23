'''
def func(x):    #og method
    return x+5

print(func(7))
'''

'''
func2=lambda x: x+5     #lambda
print(func2(7))
'''

'''
def func(x):
    func2= lambda x: x+5    #nested funcs
    return func2(x) + 8

print(func(7))
'''

'''
func3= lambda x,y : x+y     #can use multiple parameters
print(func3(3,5))
'''

'''
func3 = lambda x,y=4: x+y   # we can also use optional parameters
print(func3(6))
'''
#uses of map() and filter()
a=[1,2,3,4,5,6,7,8,9,10]

newlist=list(filter(lambda x: x%2==0,a))

print(newlist)

'''
a=[1,2,3,4,5,6,7,8,9,10]

newlist=list(map(lambda x: x+5,a))

print(newlist)
'''
