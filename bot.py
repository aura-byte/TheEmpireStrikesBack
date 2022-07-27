def do_turn(pw):

    priority = []

    for mplanet in pw.my_planets():
        for pl in pw.not_my_planets():
            distance = pw.distance(source_planet=mplanet, destination_planet=pl)
            score = pl.growth_rate() / distance

            if pl.owner() == 0:
                score = score * 1.3

            if mplanet.num_ships() < pl.num_ships():
                score = 0

            priority.append([score, mplanet, pl, distance])

    priority.sort(key=lambda y: y[0], reverse=True)

    for target in priority:
        required_fleet_size = calculate_fleet_size(target)

        # attacking_fleets = []
        counter_priority = []
        if len(pw.enemy_fleets()) > 0:
            for e_fleet in pw.enemy_fleets():
                if e_fleet.destination_planet() == target[1]:
                    # attacking_fleets.append(e_fleet)
                    for mplanet in pw.my_planets():
                        distance = pw.distance(source_planet=mplanet, destination_planet=e_fleet.source_planet())
                        counter_priority.append([0, mplanet, e_fleet.source_planet(), distance])
                    break

        if len(counter_priority) > 0:
            counter_priority.sort(key=lambda y: y[1], reverse=True)
        for counter_target in counter_priority:
            required_fleet_size = calculate_fleet_size(counter_target)
            if counter_target[1].num_ships() > required_fleet_size * 1.5:
                pw.issue_order(source_planet=counter_target[1], destination_planet=counter_target[2], num_ships=required_fleet_size)
                return

        if target[1].num_ships() > required_fleet_size * 1.5:
            pw.issue_order(source_planet=target[1], destination_planet=target[2], num_ships=required_fleet_size)
            return


def calculate_fleet_size(target):
    if target[2].owner() == 2:
        required_fleet_size = target[2].num_ships() + (target[3] // 1.05) * target[2].growth_rate()
    else:
        required_fleet_size = target[2].num_ships() * 1.1
    return required_fleet_size
