def create_custom_dag_permission_view(self):
    '\n        Workflow:\n        1. when scheduler found a new dag, we will create an entry in ab_view_menu\n        2. we fetch all the roles associated with dag users.\n        3. we join and create all the entries for ab_permission_view_menu\n           (predefined permissions * dag-view_menus)\n        4. Create all the missing role-permission-views for the ab_role_permission_views\n\n        :return: None.\n        '
    logging.info('Fetching a set of all permission, view_menu from FAB meta-table')

    def merge_pv(perm, view_menu):
        "Create permission view menu only if it doesn't exist"
        if (view_menu and perm and ((view_menu, perm) not in all_pvs)):
            self._merge_perm(perm, view_menu)
    all_pvs = set()
    for pv in self.get_session.query(self.permissionview_model).all():
        if (pv.permission and pv.view_menu):
            all_pvs.add((pv.permission.name, pv.view_menu.name))
    for dag in dag_vms:
        for perm in dag_perms:
            merge_pv(perm, dag)
    all_dags_models = settings.Session.query(models.DagModel).filter(or_(models.DagModel.is_active, models.DagModel.is_paused)).filter((~ models.DagModel.is_subdag)).all()
    for dag in all_dags_models:
        for perm in dag_perms:
            merge_pv(perm, dag.dag_id)
    all_roles = self.get_all_roles()
    user_role = self.find_role('User')
    dag_role = [role for role in all_roles if (role.name not in EXISTING_ROLES)]
    update_perm_views = []
    dag_vm = self.find_view_menu('all_dags')
    ab_perm_view_role = sqla_models.assoc_permissionview_role
    perm_view = self.permissionview_model
    view_menu = self.viewmenu_model
    all_perm_view_by_user = settings.Session.query(ab_perm_view_role).join(perm_view, (perm_view.id == ab_perm_view_role.columns.permission_view_id)).filter((ab_perm_view_role.columns.role_id == user_role.id)).join(view_menu).filter((perm_view.view_menu_id != dag_vm.id))
    all_perm_views = set([role.permission_view_id for role in all_perm_view_by_user])
    for role in dag_role:
        existing_perm_view_by_user = self.get_session.query(ab_perm_view_role).filter((ab_perm_view_role.columns.role_id == role.id))
        existing_perms_views = set([role.permission_view_id for role in existing_perm_view_by_user])
        missing_perm_views = (all_perm_views - existing_perms_views)
        for perm_view_id in missing_perm_views:
            update_perm_views.append({
                'permission_view_id': perm_view_id,
                'role_id': role.id,
            })
    self.get_session.execute(ab_perm_view_role.insert(), update_perm_views)
    self.get_session.commit()