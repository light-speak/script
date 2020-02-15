from flask import *  # 导入Flask中的蓝图Blueprint模块

import control
from model.sport_admin import SportAdmin
from model.test_food import TestFood
from tool.handle import str_md5

test_food = Blueprint("test_food", __name__)  # 实例化一个蓝图（Blueprint）对象


@test_food.route('/test/food', methods=['post'])  # 这里添加路由和视图函数的时候与在Flask对象中添加是一样的
def food():
    foods = TestFood.query.filter(TestFood.food_price < 30).order_by(TestFood.food_price.asc()).all()
    food_list = []
    select_list = []
    for a_food in foods:
        food_list.append(a_food)
    for menu in food_list:
        if menu.food_price >= 20:
            result = menu.food_name + ":" + str(menu.food_price)
            select_list.append(result)
        else:
            for menu2 in food_list:
                sum=menu.food_price+menu2.food_price
                if sum>=20 and sum <=30:
                    result = menu.food_name+menu2.food_name + ":" + str(sum)
                    select_list.append(result)
                elif sum<20:
                    for menu3 in food_list:
                        sum = menu.food_price + menu2.food_price+menu3.food_price
                        if sum>=20 and sum <=30:
                            result = menu.food_name + menu2.food_name+ menu3.food_name + ":" + str(sum)
                            select_list.append(result)

    return control.success(select_list)


