// -*- coding: utf-8 -*-
// Part of Softhealer Technologies.


import { patch } from "@web/core/utils/patch";
import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";

patch(PosOrderline.prototype, {
    set_salesperson(userId) {
        this.sh_salesperson_id = userId;
        console.log("hellooooo",userId)
    },

}); 
