%define		pkgname	libmpd
Summary:	A Haskell binding to the libmpd graphics library
Name:		ghc-%{pkgname}
Version:	0.9.1.0
Release:	2
License:	BSD
Group:		Development/Languages
Source0:	http://hackage.haskell.org/packages/archive/%{pkgname}/%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	41a00cf7bc919d8ee3cdb7c21e5436a2
Patch0:		ghc-8.10.patch
URL:		http://hackage.haskell.org/package/libmpd/
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-attoparsec >= 0.10.1
BuildRequires:	ghc-base >= 4.9
BuildRequires:	ghc-bytestring >= 0.9
BuildRequires:	ghc-containers >= 0.3
BuildRequires:	ghc-data-default-class >= 0.0.1
BuildRequires:	ghc-filepath >= 1
BuildRequires:	ghc-mtl >= 2.0
BuildRequires:	ghc-network >= 2.6.3.5
BuildRequires:	ghc-safe-exceptions >= 0.1
BuildRequires:	ghc-safe-exceptions >= 0.1
BuildRequires:	ghc-text >= 0.11
BuildRequires:	ghc-time >= 1.5
BuildRequires:	ghc-utf8-string >= 0.3.1
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires:	ghc-attoparsec >= 0.10.1
Requires:	ghc-base >= 4.9
Requires:	ghc-bytestring >= 0.9
Requires:	ghc-containers >= 0.3
Requires:	ghc-data-default-class >= 0.0.1
Requires:	ghc-filepath >= 1
Requires:	ghc-mtl >= 2.0
Requires:	ghc-network >= 2.6.3.5
Requires:	ghc-safe-exceptions >= 0.1
Requires:	ghc-safe-exceptions >= 0.1
Requires:	ghc-text >= 0.11
Requires:	ghc-time >= 1.5
Requires:	ghc-utf8-string >= 0.3.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

%description
A Haskell binding to the libmpd graphics library.

%package doc
Summary:	HTML documentation for %{pkgname}
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla %{pkgname}
Group:		Documentation

%description doc
HTML documentation for %{pkgname}.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

%build
runhaskell Setup.lhs configure -v2 \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs build
runhaskell Setup.lhs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.lhs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
rm -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs register \
	--gen-pkg-config=$RPM_BUILD_ROOT/%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
