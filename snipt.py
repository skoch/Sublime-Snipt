import sublime, sublime_plugin, urllib2, json, os, re

class SyncSniptCommand(sublime_plugin.TextCommand):

    def get_userdata(self):
        # snipt plugin settings
        self.settings = sublime.load_settings("Snipt.sublime-settings")
        self.username = self.settings.get('snipt_username')
        self.userid = self.settings.get('snipt_userid')
        self.apikey = self.settings.get('snipt_apikey')
        if (not self.userid):
            sublime.error_message('No snipt.net userid. You must first set your userid in: Sublime Text2 ~> Preferences ~> Package Settings ~> Snipt Tools ~> Settings')
            return

        if (not self.username):
            sublime.error_message('No snipt.net username. You must first set your username in: Sublime Text2 ~> Preferences ~> Package Settings ~> Snipt Tools ~> Settings')
            return

        if (not self.apikey):
            sublime.error_message('No snipt.net apikey. You must first set your apikey in: Sublime Text2 ~> Preferences ~> Package Settings ~> Snipt Tools ~> Settings')
            return

    def run(self, edit):

        # check for id config
        self.get_username()

        username = self.username
        id = self.userid
        apikey = self.apikey

        # grab the user's public snipts
        try:
            response = urllib2.urlopen('https://snipt.net/api/public/snipt/?user=%s&format=json' % id)
        except urllib2.URLError, (err):
            sublime.error_message("Error getting public snipts. (1)")
            return

            # grab all user snipt #'s
            parse = json.load(response)
            objects = parse['objects']

            # run the loop
            for item in objects:
                title = item['title']
                code = item['code']

                rx = re.compile('\W+')
                cleantitle = rx.sub(' ', title).strip()

                buildfile = 'repo/%s.sublime-snippet' % cleantitle[0:20]
                newfile = open(buildfile,'w+')
                newfile.write('<snippet><content><![CDATA[%s]]></content><tabTrigger>snipt</tabTrigger></snippet>' % code)
                newfile.close()