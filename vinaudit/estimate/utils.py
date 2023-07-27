
def check_data(year, make, model, mileage):
    data = {}
    if not year:
        return "year should be integer", data
    
    if not make or type(make) != str:
        return "make should be integer", data
    
    if not model or type(model) != str:
        return "model should be integer", data
    
    if mileage and type(mileage) != int:
        return "mileage should be integer", data
    
    data["year"] = year
    data["make"] = make.lower()
    data["model"] = model.lower()
    data["mileage"] = mileage
    return None, data


def check_input_file(keys=[]):
    all_keys = ["vin" ,"year", "make", "model", "trim", "dealer_name", "dealer_street", "dealer_city", "dealer_state",
                    "dealer_zip", "listing_price", "listing_mileage", "used", "certified", "style", "driven_wheels",
                        "engine", "fuel_type", "exterior_color", "interior_color", "seller_website", "first_seen_date",
                            "last_seen_date", "dealer_vdp_last_seen_date", "listing_status"]
    
    un_expected = []
    for key in keys:
        if key not in all_keys:
            tup = (key, "unexpected key")
            un_expected.append(tup)
            
    for key in all_keys:
        if key not in keys:
            tup = (key, "required key")
            un_expected.append(tup)
            
    return un_expected        