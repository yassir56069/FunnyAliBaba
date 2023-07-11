from entity import entity, player
from controls import control_dsg

class bucketSets:
    def __init__(self, screen):
        self.screen = screen

    def spawnPC(self, p:player, kb:control_dsg) -> None:
   
            kb.borderAll(self.screen, p)
            kb.jumpEx(p)
            p.animChara()
            p.delayEx(100)
            p.BulletEx()

    def spawnNPC(self, kb: control_dsg) -> None:
        for n in entity.getNpcs():
            if n.show:
                kb.jumpEx(n)
                
                n.animChara()
                n.delayEx(100)
                n.BulletEx()

                kb.borderAll(self.screen, n, coords=(None, None, -1))
