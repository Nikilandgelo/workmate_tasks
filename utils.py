def raise_error_if_not_instance(instances_with_classes: list[tuple]) -> None:
    for instance in instances_with_classes:
        if not isinstance(instance[0], instance[1]):
            raise TypeError(
                (
                    f'"{instance[0]}" it`s an instance of '
                    f'"{instance[0].__class__.__name__}" class, but '
                    f'"{instance[1].__name__}" class expected.'
                )
            )
