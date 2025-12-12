def build_available_attributes(variants):
    result = {}

    for v in variants:
        for item in v.attributes.all():
            attr_id = str(item.attribute.id)

            if attr_id not in result:
                result[attr_id] = {
                    "attribute_id": attr_id,
                    "attribute_name": item.attribute.name,
                    "values": set(),
                }

            result[attr_id]["values"].add((str(item.value.id), item.value.value))

    # Convert sets → lists
    for attr in result.values():
        attr["values"] = [
            {"value_id": value_id, "value": val} for value_id, val in attr["values"]
        ]

    return result


def build_combination_map(variants):
    result = {}

    for v in variants:
        combos = []
        for item in v.attributes.all():
            combos.append(f"{item.attribute_id}:{item.value_id}")

        key = "|".join(sorted(combos))
        result[key] = str(v.id)

    return result
