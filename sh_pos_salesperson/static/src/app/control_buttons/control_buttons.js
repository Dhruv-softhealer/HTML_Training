

import { patch } from "@web/core/utils/patch";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { makeAwaitable } from "@point_of_sale/app/store/make_awaitable_dialog";
import { SelectionPopup } from "@point_of_sale/app/utils/input_popups/selection_popup";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";

patch(ControlButtons.prototype, {
    setup() {
        super.setup?.();
        this.dialog = useService("dialog");
        this.notification = useService("notification");
    },

    async onClickSalesperson() {
        console.log("hyyyyyyyyy")
        const users = await this.pos.data.call("res.users", "search_read", [
            [["active", "=", true]],
            ["name"],
        ]);
        console.log("users----------->>>",users)
        this.pos.users = users;

        const userList = this.pos.users.map((user) => ({
            id: user.id,
            label: user.name,
            isSelected: false,
            item: user,
        }));

        const result = await makeAwaitable(this.dialog, SelectionPopup, {
            title: _t("Select Salesperson"),
            list: userList,
        });

        console.log("===============",userList);

        if (result) {
            console.log("user selected",result)
            const selectedUser = result;
            const orderline = this.pos.get_order()?.get_selected_orderline();
            console.log("============orderline==========",orderline)
            if (orderline) {
                console.log("fsdjfvsfbvkj==-=-=-=-=-=-")
                let user  = this.pos.models["res.users"].get(selectedUser.id)
                orderline.set_salesperson(user);
                this.notification.add(`Salesperson set to ${selectedUser.name}`, { type: "success" });
            }
        }
    },
});
