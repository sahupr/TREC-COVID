import json

COMBINE_RUN_SETTING_FILENAME = 'combine_run_settings_rnd_4.json'

if __name__ == '__main__':
    with open(COMBINE_RUN_SETTING_FILENAME) as json_file:
        settings = json.load(json_file)
    for setting in settings:
        print(setting['run_tag'])
        with open(setting['run_1_filename']) as run_1_file, open(setting['run_2_filename']) as run_2_file, open(setting['output_filename'], 'w') as output_file:
            rank_lists = {}
            boost_sets = {}
            for line in run_1_file:
                tokens = line.split()
                topic_id = int(tokens[0])
                cord_uid = tokens[2]
                if topic_id not in rank_lists:
                    rank_lists[topic_id] = []
                rank_lists[topic_id].append(cord_uid)
            for line in run_2_file:
                tokens = line.split()
                topic_id = int(tokens[0])
                cord_uid = tokens[2]
                if topic_id not in boost_sets:
                    boost_sets[topic_id] = set()
                boost_sets[topic_id].add(cord_uid)
            for topic_id in sorted(rank_lists.keys()):
                upboosted_cord_uids = [cord_uid for cord_uid in rank_lists[topic_id] if topic_id in boost_sets and cord_uid in boost_sets[topic_id]]
                downboosted_cord_uids = [cord_uid for cord_uid in rank_lists[topic_id] if topic_id not in boost_sets or cord_uid not in boost_sets[topic_id]]
                new_rank_list = upboosted_cord_uids + downboosted_cord_uids
                for (counter, cord_uid) in enumerate(new_rank_list):
                    output_file.write('{} Q0 {} {} {} {}\n'.format(topic_id, cord_uid, counter + 1, 1 - counter / 1000, setting['run_tag']))
