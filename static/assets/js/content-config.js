var globalConfig = {
  round_number: 1,
  tabs: [
    {
      content: [
        {
          label: {
            title: 'Parte I',
          },
          questions: [
            {
              text: 'Sesión Preliminar con el solicitante',
              isSubTitle: true,
            },
            {
              text: 'El facilitador se presentó e inició de manera respetuosa, amable y buscando confianza del solicitante',
              isSubTitle: false,
            },

            {
              text: 'Explicó las características de los MASC:',
              isSubTitle: true,
            },
            {
              text: 'Cuáles son los MASC y en qué consisten ',
              isSubTitle: false,
            },
            {
              text: 'El rol del facilitador en cada uno de los mecanismos',
              isSubTitle: false,
            },

            {
              text: 'Explicó detalladamente los principios de los MASC:',
              isSubTitle: true,
            },
            {
              text: 'Voluntariedad',
              isSubTitle: false,
            },
            {
              text: 'Información',
              isSubTitle: false,
            },
            {
              text: 'Confidencialidad',
              isSubTitle: false,
            },
            {
              text: 'Flexibilidad y simplicidad',
              isSubTitle: false,
            },
            {
              text: 'Imparcialidad',
              isSubTitle: false,
            },
            {
              text: 'Equidad',
              isSubTitle: false,
            },
            {
              text: 'Honestidad',
              isSubTitle: false,
            },

            {
              text: 'El facilitador ',
              isSubTitle: true,
            },
            {
              text: 'Explicó los derechos y obligaciones de los intervinientes ',
              isSubTitle: false,
            },
            {
              text: 'Logró transmitir las ventajas de la mediación para garantizar su participación en ella',
              isSubTitle: false,
            },
            {
              text: 'Expuso las formas de comunicarse y conducirse en la sesión conjunta',
              isSubTitle: false,
            },
            {
              text: 'El facilitador se desempeñó con seguridad',
              isSubTitle: false,
            },
            {
              text: 'Obtuvo la aceptación a sujetarse al proceso del solicitante',
              isSubTitle: false,
            },

            {
              text: 'Notoriamente hizo uso de sus habilidades de escucha:',
              isSubTitle: true,
            },
            {
              text: 'Hizo contacto visual apropiado',
              isSubTitle: false,
            },
            {
              text: 'Con su lenguaje corporal',
              isSubTitle: false,
            },
            {
              text: 'Parafraseó el diálogo con precisión',
              isSubTitle: false,
            },
            {
              text: 'Hizo un reencuadre apropiado',
              isSubTitle: false,
            },
            {
              text: 'Identificó el o los intereses del solicitante',
              isSubTitle: false,
            },
            {
              text: 'Extrajo la información suficiente del conflicto',
              isSubTitle: false,
            },
            {
              text: 'Hizo una transición apropiada para la sesión conjunta',
              isSubTitle: false,
            },
            {
              text: 'Creó un ambiente seguro y confiable para el solicitante ',
              isSubTitle: false,
            },
          ],
        },
        {
          label: {
            title: 'Parte II',
          },
          questions: [],
        },
        {
          label: {
            title: 'Parte III',
          },
          questions: [],
        },
        {
          label: {
            title: 'Parte IV',
          },
          questions: [],
        },
      ],
    },
    {
      content: [
        {
          label: {
            title: 'Parte I',
          },
          questions: [
            {
              text: 'Second round',
              isSubTitle: true,
            },
            {
              text: 'Question one',
              isSubTitle: false,
            },
          ]
        },
        {
          label: {
            title: 'Parte II',
          },
          questions: [
            {
              text: 'Second round tab',
              isSubTitle: true,
            },
            {
              text: 'Question one',
              isSubTitle: false,
            },
          ]
        },
      ]
    },
    {
      content: [
        {
          label: {
            title: 'Parte I',
          },
          questions: [
            {
              text: 'Question one I',
              isSubTitle: false,
            },
          ],
        },
        {
          label: {
            title: 'Parte II',
          },
          questions: [
            {
              text: 'Question one II',
              isSubTitle: false,
            },
          ],
        },
        {
          label: {
            title: 'Parte III',
          },
          questions: [
            {
              text: 'Question one III',
              isSubTitle: false,
            },
          ],
        },
        {
          label: {
            title: 'Parte IV',
          },
          questions: [
            {
              text: 'Question one IV',
              isSubTitle: false,
            },
          ],
        },
      ],
    },
    {
      content: [
        {
          label: {
            title: 'Parte I',
          },
          questions: [
            {
              text: 'Question one I',
              isSubTitle: false,
            },
          ],
        },
        {
          label: {
            title: 'Parte II',
          },
          questions: [
            {
              text: 'Question one II',
              isSubTitle: false,
            },
          ],
        },
        {
          label: {
            title: 'Parte III',
          },
          questions: [
            {
              text: 'Question one III',
              isSubTitle: false,
            },
          ],
        },
        {
          label: {
            title: 'Parte IV',
          },
          questions: [
            {
              text: 'Question one IV',
              isSubTitle: false,
            },
          ],
        },
      ],
    },
    {
      content: [
        {
          label: {
            title: 'Parte I',
          },
          questions: [
            {
              text: 'Question one I',
              isSubTitle: false,
            },
          ],
        },
        {
          label: {
            title: 'Parte II',
          },
          questions: [
            {
              text: 'Question one II',
              isSubTitle: false,
            },
          ],
        },
        {
          label: {
            title: 'Parte III',
          },
          questions: [
            {
              text: 'Question one III',
              isSubTitle: false,
            },
          ],
        },
        {
          label: {
            title: 'Parte IV',
          },
          questions: [
            {
              text: 'Question one IV',
              isSubTitle: false,
            },
          ],
        },
      ],
    },
  ]
};

for (var roundId = 0; roundId < globalConfig.tabs.length ; roundId++) {
	var content = globalConfig.tabs[roundId].content
  globalConfig.tabs[roundId].id = roundId

  for (var tabId = 0; tabId < content.length ; tabId++) {
    content[tabId].id = roundId + '-' + tabId
    content[tabId].questions = content[tabId].questions.map(function (question, idx) {
      return {
        index: roundId + '-' + tabId + '-' + idx,
        text: question.text,
        isSubTitle: question.isSubTitle,
      }
    })
  }
}

var roundScores = [
  {
    roundId: 1,
    teams: [
      {
        id: 1,
        scores: []
      }
    ]
  },
  {
    roundId: 2,
    teams: [
      {
        id: 1,
        scores: []
      },
      {
        id: 2,
        scores: []
      }
    ]
  },
  {
    roundId: 3,
    teams: [
      {
        id: 1,
        scores: []
      },
      {
        id: 2,
        scores: []
      }
    ]
  },
  {
    roundId: 4,
    teams: [
      {
        id: 1,
        scores: []
      },
      {
        id: 2,
        scores: []
      }
    ]
  },
  {
    roundId: 5,
    teams: [
      {
        id: 1,
        scores: []
      },
      {
        id: 2,
        scores: []
      }
    ]
  },
]

for (var roundId = 0; roundId < roundScores.length; roundId++) {
	var round = roundScores[roundId]

  for (var teamId = 0; teamId < round.teams.length ; teamId++) {
  	var team = round.teams[teamId]

    for (let tabId = 0; tabId < globalConfig.tabs[roundId].content.length; tabId++) {
      team.scores.push({
        tabId: globalConfig.tabs[roundId].id,
        ratings: [],
      })
    }
  }
}
