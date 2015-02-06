class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @classmethod
    def disable(cls):
        cls.HEADER = ""
        cls.BLUE = ""
        cls.GREEN = ""
        cls.RED = ""
        cls.END = ""
        cls.BOLD = ""
        cls.UNDERLINE = ""

vampygarou_msg = r"""
                             *    (       )               (       )
             (     (  `   )\ ) ( /( (       (     )\ ) ( /(
     (   (   )\    )\))( (()/( )\()))\ )    )\   (()/( )\())    (
     )\  )((((_)( ((_)()\ /(_)|(_)\(()/( ((((_)(  /(_)|(_)\     )\
    ((_)((_)\ _ )\(_()((_|_))__ ((_)/(_))_)\ _ )\(_))   ((_) _ ((_)
    \ \ / /(_)_\(_)  \/  | _ \ \ / (_)) __(_)_\(_) _ \ / _ \| | | |
     \ V /  / _ \ | |\/| |  _/\ V /  | (_ |/ _ \ |   /| (_) | |_| |
      \_/  /_/ \_\|_|  |_|_|   |_|    \___/_/ \_\|_|_\ \___/ \___/



                                      _.-.
                                 ._.-.\
                    .^         _.-'=. \\
                  .'  )    .-._.-=-..' \'.
               .'   .'   _.--._-='.'   |  `.  ^.
             .'   .'    _`.-.`=-./'.-. / .-.\ `. `.
           .'    /      _.-=-=-/ | '._)`(_.'|   \  `.
          /    /|       _.--=.'  `. (.-v-.)/    |\   \
        .'    / \       _.-.' \-.' `-..-..'     / \   `.
       /     /   `-.._ .-.'      `.'  " ". _..-'  |    |
      '      |    |   /   )        \  /   \   \    \    `.
     /      /    /   /   /\                \   \   |      \
    /      /    /  .'  .'\ `.        .'     \   |   \      \
   /      /    /  /   /   \  `-    -' .`.    .  \    \     |
  |      /    / .''\.'    | `.      .'   `.   \  |    |    |
 .'     /    / /   |      |      .'/       `.- `./    /    |
 |     /    .-|   /--.    / `.    |    _.-''\   |     |    \
.'    /  .-'  |  /    `-.|       .'\_.'      `. |`.   |    |
|    |.-'     / /       /           \          \ \ `. \     \
|    /       /  |      /             \         |  `. `.|    |
|   |       /   `.     |      `   .'  \        /    \  \    /
|   |      ///.-'.\    |       \ /    `\      / /-.  \ |    |
|   /      \\\\    `    \.-     |    `-.\     |/   \\\\'.   |
 \ |        \\\|        |      / \      |          //// |  /
 | |         '''        |     /   \     |          |//  |  \
 \ |                    |.-  |     \  .-|          ''   |  /
  \|                    /    |    / ` ../               / /
                        |'   /    |    /               | /
                        \.'  |    | `./                |/
                        /    \   /    \
                        \ `. /   \    /
                         |  |     '. '
                         /  |      |  \
                        /   |      /   `.
                       | | | \   .'  `.. \
                      / / / ._`. \.'-. \`/
                      |/ / /  `'  `  |/|/
                       \|\|
"""
