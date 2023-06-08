// Generated from /home/marc/Disco/UNIVERSITAT/Tercer_any/Practica_LP/lc.g4 by ANTLR 4.9.2
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class lcParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.9.2", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, T__1=2, T__2=3, MACRO=4, LLETRA=5, LLETRAMAJUSCULA=6, DIGIT=7, 
		LAMBDA=8, ASSIGNACIO=9, WS=10;
	public static final int
		RULE_root = 0, RULE_terme = 1, RULE_assignacio = 2;
	private static String[] makeRuleNames() {
		return new String[] {
			"root", "terme", "assignacio"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'('", "')'", "'.'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, null, null, "MACRO", "LLETRA", "LLETRAMAJUSCULA", "DIGIT", 
			"LAMBDA", "ASSIGNACIO", "WS"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}

	@Override
	public String getGrammarFileName() { return "lc.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public lcParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	public static class RootContext extends ParserRuleContext {
		public TermeContext terme() {
			return getRuleContext(TermeContext.class,0);
		}
		public AssignacioContext assignacio() {
			return getRuleContext(AssignacioContext.class,0);
		}
		public RootContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_root; }
	}

	public final RootContext root() throws RecognitionException {
		RootContext _localctx = new RootContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_root);
		try {
			setState(8);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,0,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(6);
				terme(0);
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(7);
				assignacio();
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class TermeContext extends ParserRuleContext {
		public TermeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_terme; }
	 
		public TermeContext() { }
		public void copyFrom(TermeContext ctx) {
			super.copyFrom(ctx);
		}
	}
	public static class ParentesisContext extends TermeContext {
		public TermeContext terme() {
			return getRuleContext(TermeContext.class,0);
		}
		public ParentesisContext(TermeContext ctx) { copyFrom(ctx); }
	}
	public static class MacroContext extends TermeContext {
		public TerminalNode MACRO() { return getToken(lcParser.MACRO, 0); }
		public MacroContext(TermeContext ctx) { copyFrom(ctx); }
	}
	public static class VariableContext extends TermeContext {
		public TerminalNode LLETRA() { return getToken(lcParser.LLETRA, 0); }
		public VariableContext(TermeContext ctx) { copyFrom(ctx); }
	}
	public static class AbstraccioContext extends TermeContext {
		public TerminalNode LAMBDA() { return getToken(lcParser.LAMBDA, 0); }
		public TermeContext terme() {
			return getRuleContext(TermeContext.class,0);
		}
		public List<TerminalNode> LLETRA() { return getTokens(lcParser.LLETRA); }
		public TerminalNode LLETRA(int i) {
			return getToken(lcParser.LLETRA, i);
		}
		public AbstraccioContext(TermeContext ctx) { copyFrom(ctx); }
	}
	public static class AplicacioContext extends TermeContext {
		public List<TermeContext> terme() {
			return getRuleContexts(TermeContext.class);
		}
		public TermeContext terme(int i) {
			return getRuleContext(TermeContext.class,i);
		}
		public AplicacioContext(TermeContext ctx) { copyFrom(ctx); }
	}

	public final TermeContext terme() throws RecognitionException {
		return terme(0);
	}

	private TermeContext terme(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		TermeContext _localctx = new TermeContext(_ctx, _parentState);
		TermeContext _prevctx = _localctx;
		int _startState = 2;
		enterRecursionRule(_localctx, 2, RULE_terme, _p);
		int _la;
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(25);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__0:
				{
				_localctx = new ParentesisContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;

				setState(11);
				match(T__0);
				setState(12);
				terme(0);
				setState(13);
				match(T__1);
				}
				break;
			case LAMBDA:
				{
				_localctx = new AbstraccioContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(15);
				match(LAMBDA);
				setState(17); 
				_errHandler.sync(this);
				_la = _input.LA(1);
				do {
					{
					{
					setState(16);
					match(LLETRA);
					}
					}
					setState(19); 
					_errHandler.sync(this);
					_la = _input.LA(1);
				} while ( _la==LLETRA );
				setState(21);
				match(T__2);
				setState(22);
				terme(3);
				}
				break;
			case LLETRA:
				{
				_localctx = new VariableContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(23);
				match(LLETRA);
				}
				break;
			case MACRO:
				{
				_localctx = new MacroContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(24);
				match(MACRO);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
			_ctx.stop = _input.LT(-1);
			setState(31);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,3,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					{
					_localctx = new AplicacioContext(new TermeContext(_parentctx, _parentState));
					pushNewRecursionContext(_localctx, _startState, RULE_terme);
					setState(27);
					if (!(precpred(_ctx, 5))) throw new FailedPredicateException(this, "precpred(_ctx, 5)");
					setState(28);
					terme(6);
					}
					} 
				}
				setState(33);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,3,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	public static class AssignacioContext extends ParserRuleContext {
		public TerminalNode MACRO() { return getToken(lcParser.MACRO, 0); }
		public TerminalNode ASSIGNACIO() { return getToken(lcParser.ASSIGNACIO, 0); }
		public TermeContext terme() {
			return getRuleContext(TermeContext.class,0);
		}
		public AssignacioContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_assignacio; }
	}

	public final AssignacioContext assignacio() throws RecognitionException {
		AssignacioContext _localctx = new AssignacioContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_assignacio);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(34);
			match(MACRO);
			setState(35);
			match(ASSIGNACIO);
			setState(36);
			terme(0);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public boolean sempred(RuleContext _localctx, int ruleIndex, int predIndex) {
		switch (ruleIndex) {
		case 1:
			return terme_sempred((TermeContext)_localctx, predIndex);
		}
		return true;
	}
	private boolean terme_sempred(TermeContext _localctx, int predIndex) {
		switch (predIndex) {
		case 0:
			return precpred(_ctx, 5);
		}
		return true;
	}

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\f)\4\2\t\2\4\3\t"+
		"\3\4\4\t\4\3\2\3\2\5\2\13\n\2\3\3\3\3\3\3\3\3\3\3\3\3\3\3\6\3\24\n\3\r"+
		"\3\16\3\25\3\3\3\3\3\3\3\3\5\3\34\n\3\3\3\3\3\7\3 \n\3\f\3\16\3#\13\3"+
		"\3\4\3\4\3\4\3\4\3\4\2\3\4\5\2\4\6\2\2\2+\2\n\3\2\2\2\4\33\3\2\2\2\6$"+
		"\3\2\2\2\b\13\5\4\3\2\t\13\5\6\4\2\n\b\3\2\2\2\n\t\3\2\2\2\13\3\3\2\2"+
		"\2\f\r\b\3\1\2\r\16\7\3\2\2\16\17\5\4\3\2\17\20\7\4\2\2\20\34\3\2\2\2"+
		"\21\23\7\n\2\2\22\24\7\7\2\2\23\22\3\2\2\2\24\25\3\2\2\2\25\23\3\2\2\2"+
		"\25\26\3\2\2\2\26\27\3\2\2\2\27\30\7\5\2\2\30\34\5\4\3\5\31\34\7\7\2\2"+
		"\32\34\7\6\2\2\33\f\3\2\2\2\33\21\3\2\2\2\33\31\3\2\2\2\33\32\3\2\2\2"+
		"\34!\3\2\2\2\35\36\f\7\2\2\36 \5\4\3\b\37\35\3\2\2\2 #\3\2\2\2!\37\3\2"+
		"\2\2!\"\3\2\2\2\"\5\3\2\2\2#!\3\2\2\2$%\7\6\2\2%&\7\13\2\2&\'\5\4\3\2"+
		"\'\7\3\2\2\2\6\n\25\33!";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}