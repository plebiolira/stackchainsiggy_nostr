def extract_note_id_to_stackjoinadd(event_msg: list):
    # upon confirming it's a new event, checking if it's a reply or a new note
    non_mention_e_tags = []
    for tag in event_msg.event.json[2]["tags"]:
        if "e" in tag and "mention" not in tag:
            non_mention_e_tags.append(tag)
    if len(non_mention_e_tags) == 1:
        print("single non_mention tag, means it's the note to be retrieved")
        query_term = non_mention_e_tags[0][1]
    else:
    # more than 1 non_mention tag, verifying which one is the reply and which one is the root
        for tag in non_mention_e_tags:
            if "root" in tag or "reply" in tag:
                print('using marked "e" tags')
            if "reply" in tag:
                query_term = tag[1]
            else:
                print('using positional "e" tags')
                query_term = non_mention_e_tags[1][1]
    if non_mention_e_tags == []:
        print("new note")
        query_term = event_msg.event.json[2]["id"]

    return query_term