
LCI - A lambda calculus interpreter
Copyright (C) 2004-8 Kostas Chatzikokolakis

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

----------------------------------------------------------------------------------

NOTE - Binary Distribution

This is a binary distribution of lci for win32 built with cygwin. The distribution
contains also some parts of the cygwin environment needed to run the program.
You can find the source code of lci at http://lci.sourceforge.net/ and the source
code of cygwin at http://www.cygwin.com/.

To execute the program simply open the directory where you extracted the
archive and run
  lci.exe
The remaining of this README refers to the source distribution, some
paragraphs (eg compilation) might not apply to the binary one.

----------------------------------------------------------------------------------

What is LCI?

LCI is an interpreter for the lambda calculus. It was first developed as an
assignment for the "Theory of Programming Languages" course in University of
Athens. Later it became open source software licenced under GPL and many
advanced features were added:

- Supports aliases of lambda terms (that is named functions)
- Supports integers coded as church numerals.
  All operations are implemented in the pure calculus
- Supports recursion. It can also automatically convert recursive terms to
  non-recursive ones using a fixed point combinator.
- Supports user-defined operators, which means that the user can declare a new
  operator with a certain precedence and associativity and define it in lambda
  calculus. Many common operators (eg. integer, logic and list operations) are
  pre-defined in .lcirc file and are available by default.
- Supports multiple evaluation strategies. Call-by-name and call-by-value can
  coexist in the same program.
- Supports human-readable display of terms: for example church numerals are
  displayed as numbers and lists using the [a,b,c] notation.
- Supports tracing of execution.
- Supports file interpretation as well as interactive usage.
- Comes with a "library" of pre-defined functions (.lcirc file)

Due to its advanced features lci can be considered as a small (but powerfull enough)
functional progamming language based on lambda-calculus. To demonstrate its
capabilities there is an implementation of n-Queens problem (queens.lci file) in a
way very similar to Haskell syntax. However all features are implemented using the
pure calculus.

----------------------------------------------------------------------------------

Installation

You can compile LCI in the standard unix way by executing
   ./configure
   make
An executable named "lci" will be created in the src directory, you can run it from
there or you can install it in your system by executing
   make install
This will install lci executable in /usr/local/bin and .lcirc, queens.lci in
/usr/local/share/lci. You can install lci in a different location by passing
a --prefix=<dir> argument to ./confugure. See INSTALL for more info.

LCI has no hard dependencies (except from a descent C99 compiler, gcc is
recommended) but it is recommended to install readline before compiling
for better input handling, history, etc.

If you downloaded the code from subversion then you need to install autotools and run
./reconf to create the configure script.

----------------------------------------------------------------------------------

Directory structure

/		This folder contains text documents (README, TODO, licence, ...) and the
		files needed by autotools.

/src	This folder contains all source code. There is also a Makefile.am and some .lci
		files (definitions of lambda-terms)

/doc	Documentation files in TeX format (in english and greek language)

----------------------------------------------------------------------------------

Contribution

If you have found a bug please report it by adding a ticket
at LCI's development page (http://trac2.assembla.com/lci) or by sending an
e-mail to kostas-at-chatzi-dot-org. Also if you 'd like to help improving
LCI by sending patches or joining the deveopment team, you are something more than
welcome!

Finally I 'd like very much to hear from people who are actually using LCI. If
you find the program useful please let me know. Also feel free to send ideas or
suggest features that should be added in future releases.


