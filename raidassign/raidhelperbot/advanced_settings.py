class AdvancedSettings:
    """
    duration<number> - The duration of the event in minutes.
    deadline<number> - The deadline in hours before the event.
    limit<number> - The maximum amount of active sign-ups.
    lock_at_limit<boolean> - whether the event will lock when the limit is reached.
    limit_per_user<number> - The maximum amount of sign-ups per member.
    lower_limit<number> - The minimum amount of sign-ups required for the event to happen.
    allow_duplicate<boolean> - whether a member can sign up multiple times to the same class.
    horizontal_mode<boolean> - whether sign-ups will be displayed horizontally instead of vertically.
    bench_overflow<boolean> - whether sign-ups past limits will be benched or simply denied.
    queue_bench<boolean> - Changes the bench behaviour to a queue.
    vacuum<boolean> - Clears the last 10 non-event messages in the channel upon event creation.
    force_reminders<boolean/number> - Force personal reminders. Time in minutes before the event.
    pin_message<boolean> - whether this event should be pinned upon creation.
    deletion<boolean/number> - The amount of hours this event will be deleted after it concluded.
    mention_mode<boolean> - Mentions the members instead of displaying the plain name.
    preserve_order<string> - Determines the behaviour of the order numbers when members change their sign-up.
    apply_unregister<boolean> - whether the unregister role will be applied.
    apply_specreset<string> - whether the reaction/button to reset the saved spec should be applied to the event.
    spec_saving<boolean> - whether the bot should remember a members spec choice and apply it automatically.
    font_style<number> - The font style for the event title. Only applies if the title is shorter than 19 characters.
    alt_names<boolean> - whether members will be allowed to enter a custom name when signing up.
    defaults_pre_req<boolean> - whether a primary role is required to sign up with a default role (bench, late, tentative).
    show_on_overview<boolean> - whether the event will be displayed on the /overview.
    mention_leader<boolean> - whether the leaders name will be displayed as a mention.
    attendance<boolean/string> - whether this event will count towards attendance. Enter a string to set an attendance
    show_title<boolean> - whether to show the title of this event.
    show_info<boolean> - whether the info row will be shown (contains date, time and number of sign-ups).
    show_leader<boolean> - whether the event leader will be shown.
    show_counter<boolean> - whether the sign-ups counter will be shown.
    show_roles<boolean> - whether to show the role counters above the sign-up content.
    show_content<boolean> - whether the sign-ups will be displayed.
    show_classes<boolean> - whether the class fields will always be shown.
    show_emotes<boolean> - whether to show the spec emotes in front of sign-ups.
    show_numbering<boolean> - whether to show the order number in front of sign-ups.
    show_allowed<boolean> - whether to show the allowed roles in the footer if any are set.
    show_footer<boolean> - whether to show the event footer.
    info_variant<string> - whether the info field will be displayed in a short or long format.
    date_variant<string> - whether the date & time on the event will be shown in the users local or zoned time.
    show_countdown<boolean> - whether to show a countdown to the event start.
    disable_archiving<boolean> - If archiving is enabled on your server you can exempt a specific event with this setting.
    bold_all<boolean> - Set to false to not count consecutive sign-ups by a user to be counted towards limits.
    bench_emote<string> - The emote id that will be used for the bench role. Set to "remove" to disable the role.
    late_emote<string> - The emote id that will be used for the late role. Set to "remove" to disable the role.
    tentative_emote<string> - The emote id that will be used for the tentative role. Set to "remove" to disable the role.
    absence_emote<string> - The emote id that will be used for the absence role. Set to "remove" to disable the role.
    leader_emote<string> - The emote id that will be used for the leader icon.
    signups1_emote<string> - The emote id that will be used for the signups icon.
    signups2_emote<string> - The emote id that will be used for the signups icon.
    date1_emote<string> - The emote id that will be used for the date icon.
    date2_emote<string> - The emote id that will be used for the date icon.
    time1_emote<string> - The emote id that will be used for the time icon.
    time2_emote<string> - The emote id that will be used for the time icon.
    countdown1_emote<string> - The emote id that will be used for the countdown icon.
    countdown2_emote<string> - The emote id that will be used for the countdown icon.
    specreset_emote<string> - The emote id that will be used for the specreset icon.
    unregister_emote<string> - The emote id that will be used for the unregister icon.
    event_type<string> - whether this event will use interactions or reactions.
    reminder<number/boolean> - Set the amount of minutes before the event a reminder will be sent.
    create_discordevent<boolean> - whether a discord integrated event should be created (requires premium).
    create_thread<boolean> - whether a thread should be created on the event.
    delete_thread<boolean> - whether the attached thread should be deleted if the event gets deleted.
    voice_channel<string> - The voicechannel used for this event.
    temp_voicechannel<string> - The name for a voicechannel that will be temporarily created.
    color<string> - The embed color for this event.
    response<string> - Enter text that will be sent to the member when they sign up.
    temp_role<string> - The name of a discord role that will be assigned to the member upon signing up.
    allowed_roles<string> - The role names that are allowed to sign up. Separate multiple names by comma.
    forum_tags<string> - The names of the forum tags that will be applied to the post. Separate multiple names by comma.
    banned_roles<string> - the role names that are banned from signing up. Separate multiple names by comma.
    opt_out<string> - The id of an existing event to copy the sign-ups from upon event creation.
    mentions<string> - The role/member names to mention upon event creation. Separate multiple names by comma.
    image<string> - The URL of an image that will be displayed at the bottom of the event embed.
    thumbnail<string> - The URL to an image which will be displayed as a thumbnail on the event embed.
    use_nicknames<string> - whether the members server nickname will be used or the global name.
    text_1<string> - replaces the 'Select your class.' text on class selection.
    text_2<string> - replaces the 'Select your spec.' text on spec selection.
    """

    def __init__(self, json_data: dict):
        """
        Initialize AdvancedSettings from a JSON object.

        Args:
            json_data (dict): A dictionary containing the advanced settings data
        """
        # Event timing and limits
        self.duration = json_data.get('duration')
        self.deadline = json_data.get('deadline')
        self.limit = json_data.get('limit')
        self.limit_per_user = json_data.get('limit_per_user')
        self.lower_limit = json_data.get('lower_limit')

        # Boolean flags for behavior
        self.lock_at_limit = json_data.get('lock_at_limit', False)
        self.allow_duplicate = json_data.get('allow_duplicate', False)
        self.horizontal_mode = json_data.get('horizontal_mode', False)
        self.bench_overflow = json_data.get('bench_overflow', False)
        self.queue_bench = json_data.get('queue_bench', False)
        self.vacuum = json_data.get('vacuum', False)
        self.pin_message = json_data.get('pin_message', False)
        self.mention_mode = json_data.get('mention_mode', False)
        self.apply_unregister = json_data.get('apply_unregister', False)
        self.spec_saving = json_data.get('spec_saving', False)
        self.alt_names = json_data.get('alt_names', False)
        self.defaults_pre_req = json_data.get('defaults_pre_req', False)
        self.show_on_overview = json_data.get('show_on_overview', False)
        self.mention_leader = json_data.get('mention_leader', False)

        # Display settings
        self.show_title = json_data.get('show_title', True)
        self.show_info = json_data.get('show_info', True)
        self.show_leader = json_data.get('show_leader', True)
        self.show_counter = json_data.get('show_counter', True)
        self.show_roles = json_data.get('show_roles', True)
        self.show_content = json_data.get('show_content', True)
        self.show_classes = json_data.get('show_classes', True)
        self.show_emotes = json_data.get('show_emotes', True)
        self.show_numbering = json_data.get('show_numbering', True)
        self.show_allowed = json_data.get('show_allowed', True)
        self.show_footer = json_data.get('show_footer', True)
        self.show_countdown = json_data.get('show_countdown', False)
        self.disable_archiving = json_data.get('disable_archiving', False)
        self.bold_all = json_data.get('bold_all', True)

        # Emote settings
        self.bench_emote = json_data.get('bench_emote')
        self.late_emote = json_data.get('late_emote')
        self.tentative_emote = json_data.get('tentative_emote')
        self.absence_emote = json_data.get('absence_emote')
        self.leader_emote = json_data.get('leader_emote')
        self.signups1_emote = json_data.get('signups1_emote')
        self.signups2_emote = json_data.get('signups2_emote')
        self.date1_emote = json_data.get('date1_emote')
        self.date2_emote = json_data.get('date2_emote')
        self.time1_emote = json_data.get('time1_emote')
        self.time2_emote = json_data.get('time2_emote')
        self.countdown1_emote = json_data.get('countdown1_emote')
        self.countdown2_emote = json_data.get('countdown2_emote')
        self.specreset_emote = json_data.get('specreset_emote')
        self.unregister_emote = json_data.get('unregister_emote')

        # Event configuration
        self.event_type = json_data.get('event_type')
        self.reminder = json_data.get('reminder')
        self.create_discordevent = json_data.get('create_discordevent', False)
        self.create_thread = json_data.get('create_thread', False)
        self.delete_thread = json_data.get('delete_thread', False)

        # Channel and role settings
        self.voice_channel = json_data.get('voice_channel')
        self.temp_voicechannel = json_data.get('temp_voicechannel')
        self.temp_role = json_data.get('temp_role')
        self.allowed_roles = json_data.get('allowed_roles')
        self.banned_roles = json_data.get('banned_roles')

        # Visual and text settings
        self.color = json_data.get('color')
        self.image = json_data.get('image')
        self.thumbnail = json_data.get('thumbnail')
        self.use_nicknames = json_data.get('use_nicknames')
        self.text_1 = json_data.get('text_1')
        self.text_2 = json_data.get('text_2')

        # Additional settings
        self.force_reminders = json_data.get('force_reminders')
        self.deletion = json_data.get('deletion')
        self.preserve_order = json_data.get('preserve_order')
        self.apply_specreset = json_data.get('apply_specreset')
        self.font_style = json_data.get('font_style')
        self.attendance = json_data.get('attendance')
        self.info_variant = json_data.get('info_variant')
        self.date_variant = json_data.get('date_variant')
        self.opt_out = json_data.get('opt_out')
        self.mentions = json_data.get('mentions')
        self.forum_tags = json_data.get('forum_tags')
        self.response = json_data.get('response')
