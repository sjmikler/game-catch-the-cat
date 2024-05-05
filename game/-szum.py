class t:
    def __init__(self):
        print("t")


class e:
    def __init__(self):
        print("e")


class q(t, e):
    def __init__(self):
        t.__init__(self)
        e.__init__(self)
        # super(e).__init__()


q()
