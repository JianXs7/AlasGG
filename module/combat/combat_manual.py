from module.base.base import ModuleBase
from module.combat.assets import *


class CombatManual(ModuleBase):
    auto_mode_checked = False
    auto_mode_switched = False
    manual_executed = False

    def combat_manual_reset(self):
        self.manual_executed = False

    def handle_combat_stand_still_in_the_middle(self, auto):
        """
        Args:
            auto (str): Combat auto mode.

        Returns:
            bool: If executed
        """
        if auto != 'stand_still_in_the_middle':
            return False
        # When switching from auto to manual, fleets are usually in the middle, no need to move down
        # Otherwise fleet will be moved to the bottom
        if self.auto_mode_switched:
            return False

        self.device.long_click(MOVE_DOWN, duration=0.8)
        return True

    def handle_combat_stand_still_bottom_left(self, auto):
        """
        Args:
            auto (str): Combat auto mode.

        Returns:
            bool: If executed
        """
        if auto != 'hide_in_bottom_left':
            return False

        self.device.long_click(MOVE_LEFT_DOWN, duration=(3.5, 5.5))
        return True

    def handle_combat_stand_still_upper_left(self, auto):
        """
        Args:
            auto (str): Combat auto mode.

        Returns:
            bool: If executed
        """
        if auto != 'hide_in_upper_left':
            return False

        self.device.long_click(MOVE_LEFT_UP, duration=(1.5, 3.5))
        return True

    def handle_combat_weapon_release(self):
        from module.gg_handler.gg_data import GGData
        _ggdata = GGData(self.config).get_data()
        if _ggdata['gg_enable'] and _ggdata['gg_auto']:
            self.device.click_limit = 30
            interval = 2
        else:
            self.device.click_limit = 12
            interval = 10
        if self.appear_then_click(READY_AIR_RAID, interval=interval):
            return True
        if self.appear_then_click(READY_TORPEDO, interval=interval):
            return True

        return False

    def handle_combat_manual(self, auto):
        """
        Args:
            auto (str): Combat auto mode.

        Returns:
            bool: If executed
        """
        if self.manual_executed or not self.auto_mode_checked:
            return False

        if self.handle_combat_stand_still_in_the_middle(auto):
            self.manual_executed = True
            return True
        if self.handle_combat_stand_still_bottom_left(auto):
            self.manual_executed = True
            return True
        if self.handle_combat_stand_still_upper_left(auto):
            self.manual_executed = True
            return True

        return False
