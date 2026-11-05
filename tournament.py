import ex3
import ex4


def run_tournament(
    opponents: list[tuple[ex3.CreatureFactory, ex4.BattleStrategy]]
) -> None:
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved\n")
    participants = [
        (factory.create_base(), strategy) for factory, strategy in opponents
    ]

    try:
        for i in range(len(participants)):
            for j in range(i + 1, len(participants)):
                creature1, strat1 = participants[i]
                creature2, strat2 = participants[j]
                print("* Battle *")
                print(creature1.describe())
                print(" vs.")
                print(creature2.describe())
                print(" now fight!")
                strat1.act(creature1)
                strat2.act(creature2)
    except Exception as e:
        print(f"Battle error, aborting tournament: {e}")


def main() -> None:
    fl_factory = ex3.FlameFactory()
    trns_factory = ex3.TransformCreatureFactory()

    normal_strat = ex4.NormalStrategy()
    aggr_strat = ex4.AggressiveStrategy()

    print("Tournament 0 (basic)")
    print("[(Flameling+Normal), (Shiftling+Aggressive)]")
    run_tournament([
        (fl_factory, normal_strat),
        (trns_factory, aggr_strat),
    ])

    print("\nTournament 1 (error)")
    print("[(Shiftling+Aggressive), (Flameling+Aggressive)]")
    run_tournament([
        (trns_factory, aggr_strat),
        (fl_factory, aggr_strat),
    ])


if __name__ == "__main__":
    main()
